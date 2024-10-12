from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from account.models import Credential
from .models import Project, Client, Status, Report, Ranking
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

# Criar novo projeto
@csrf_exempt
def create_project(request):

    # Informa o metodo
    if request.method == 'POST':
        
        # TryCath
        try:

            # Carregar dados do request
            data = json.loads(request.body.decode('utf-8'))

            # Carregar dados das repartições do json
            project = data['project']
            client = data['client']
            timeline = data['timeline']

            # Inserir dados do projeto
            project = Project.objects.create(
                name = project['name'],
                key=get_random_string(length=20)
            )

            # Inserir dados do cliente
            client = Client.objects.create(
                name = client['name'],
                email = client['email']
            )
            
            # Crie os tópicos da timeline
            for timeline_count in timeline:

                # Buscar o id
                status_id = timeline_count.get('id', 0)

                # Verificar se precisa criar novo status
                if status_id == 0:

                    # Inserir dados do status
                    status = Status.objects.create(
                        name = timeline_count['name']
                    )

                else:

                    # Atualizar dados do status

                    #status = get_object_or_404(Status, id=status_id)
                    #status.name = timeline_count['name']
                    #status.save()

                    status = Status.objects.filter(id = status_id).update(
                        name = timeline_count['name']
                    )
                    status.save()

                # Inserir dados do ranking
                Ranking.objects.create(
                    project_id = project,
                    status_id = status,
                    rank = timeline_count['rank']
                )

            # Retorne uma resposta de sucesso
            response_data = {
                'message': 'Prjeto criado com sucesso'
            }

            # Retorne uma resposta de sucesso
            return JsonResponse(response_data)

        except Exception as e:
            # Em caso de qualquer exceção, retorne uma resposta de erro
            return JsonResponse({'error': str(e)}, status=500)

    # Se não for um request POST, retorne um erro de método não permitido
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def upadate_project(request):

    # Informa o metodo
    if request.method == 'POST':

        try:
            # Carregar dados do request
            data = json.loads(request.body.decode('utf-8'))

            # Carregar dados das repartições do json
            project_data = data['project']
            client_data = data['client']
            timeline = data['timeline']

            # Atualizar dados do projeto
            project = get_object_or_404(Project, id=project_data['id'])
            project.name = project_data['name']
            project.save()

            # Atualizar dados do cliente
            client = get_object_or_404(Client, id=client_data['id'])
            client.name = client_data['name']
            client.email = client_data['email']
            client.save()

            # Atualizar ou criar dados da timeline (status e ranking)
            for timeline_item in timeline:

                # Verificar se o status já existe
                status_id = timeline_item.get('id', 0)
                if status_id == 0:
                    # Criar novo status
                    status = Status.objects.create(
                        name=timeline_item['name']
                    )
                else:
                    # Atualizar status existente
                    status = get_object_or_404(Status, id=status_id)
                    status.name = timeline_item['name']
                    status.save()

                # Verificar se o ranking já existe para o status e projeto
                ranking, created = Ranking.objects.get_or_create(
                    project_id=project,
                    status_id=status
                )

                # Atualizar os dados do ranking
                ranking.rank = timeline_item['rank']
                ranking.status = timeline_item['status']  
                ranking.last_update = timeline_item['last_update']  
                ranking.save()

            # Retornar uma resposta de sucesso
            response_data = {
                'message': 'Projeto atualizado com sucesso'
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def list_details(request, project_id):

    # Informa o metodo
    if request.method == 'GET':

        try:
            # Buscar o projeto pelo ID
            project = get_object_or_404(Project, id=project_id)

            # Buscar o cliente associado ao projeto
            client = Client.objects.filter(id=project.id)

            # Buscar o ranking associado ao projeto
            rankings = Ranking.objects.filter(project_id=project)

            # Criar a lista da timeline
            timeline = []
            for ranking in rankings:
                timeline.append({
                    'id': ranking.status_id.id,
                    'name': ranking.status_id.name,
                    'rank': ranking.rank,
                    'last_update': ranking.last_update.strftime('%d/%m/%Y'),  # Formatação da data
                })

            # Montar o objeto de resposta
            response_data = {
                'project': {
                    'id': project.id,
                    'name': project.name,
                    'key': project.key,
                },
                'client': {
                    'id': client.id,
                    'name': client.name,
                    'email': client.email,
                },
                'timeline': timeline
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# ----------------------------------------------- OLD CODE -----------------------------------------------

# Atualizar dados do projeto
@csrf_exempt
def update_project(request):

    # Informar o metodo
    if request.method == 'PUT':

        try:

            data = json.loads(request.body.decode('utf-8'))
            print(f'data: {data}')

            credential_id = id
            print(f'credential_id: {credential_id}')

            # Buscar a chave do curriculo
            key = request.GET.get('key', None)

            if key:

                # Obtenha o usuário existente
                user = User.objects.get(key=key)

                user_data = data['user']
                print(f'user_data: {user_data}')

                # Atualize os campos do usuário
                user_data = data.get('user', {})

                if user_data:

                    # Atualize os campos do usuário
                    user_id = str(user.credential_id)
                    print(f'user_id: {user_id}')

                    # Verificar se usuário tem permissão para alterações
                    if user_id == credential_id:
                        user_admin = True
                    else:
                        user_admin = False
                    
                    if user_admin:
                        user.name = user_data.get('name', user.name)
                        user.title = user_data.get('title', user.title)
                        user.email = user_data.get('email', user.email)
                        user.phone = user_data.get('phone', user.phone)
                        user.location = user_data.get('location', user.location)
                        user.avatar = user_data.get('avatar', user.avatar)
                        user.gender = user_data.get('gender', user.gender)
                        user.pronoun = user_data.get('pronoun', user.pronoun)
                        user.description = user_data.get('description', user.description)
                        user.access_level = user_data.get('access_level', user.access_level)
                        user.published = user_data.get('published', user.published)
                        user.save()

                        # Buscar as informações do links
                        for link_data in data.get('links', []):
                            link_id = link_data.get('id', 0)
                            link_status = link_data.get('status', True)

                            # Atualizar os links
                            if link_id > 0:
                                if link_status == True:
                                    Link.objects.filter(user=user, id=link_id).update(
                                        name=link_data.get('name', ''),
                                        url=link_data.get('url', '')
                                    )
                                else:
                                    Link.objects.filter(user=user, id=link_id).delete()
                            else:
                                Link.objects.create(user=user, name=link_data.get('name', ''), url=link_data.get('url', ''))
                        
                        # Buscar as informações de experience
                        for exp_data in data.get('experience', []):
                            exp_id = exp_data.get('id', 0)
                            exp_status = exp_data.get('status', True)

                            # Atualizar as experience
                            if exp_id > 0:
                                if exp_status == True:
                                    Experience.objects.filter(user=user, id=exp_id).update(
                                        company=exp_data.get('company', ''),
                                        position=exp_data.get('position', ''),
                                        period=exp_data.get('period', ''),
                                        description=exp_data.get('description', '')
                                    )
                                else:
                                    Experience.objects.filter(user=user, id=exp_id).delete()
                            else:
                                Experience.objects.create(user=user, **exp_data)

                        # Buscar as informações de Educational
                        for edu_data in data.get('education', []):
                            edu_id = edu_data.get('id', 0)
                            edu_status = edu_data.get('status', True)

                            # Atualizar as educational
                            if edu_id > 0:
                                if edu_status == True:
                                    Education.objects.filter(user=user, id=edu_id).update(
                                        institution=edu_data.get('institution', ''),
                                        course=edu_data.get('course', ''),
                                        period=edu_data.get('period', ''),
                                        description=edu_data.get('description', '')
                                    )
                                else:
                                    Education.objects.filter(user=user, id=edu_id).delete()
                            else:
                                Education.objects.create(user=user, **edu_data)

                        # Busca as informação de Skill
                        for skill_data in data.get('skills', []):
                            skill_id = skill_data.get('id', 0)
                            skill_status = skill_data.get('status', True)

                            # Atualizar as skills
                            if skill_id > 0:
                                if skill_status == True:
                                    Skill.objects.filter(user=user, id=skill_id).update(
                                        name=skill_data.get('name', '')
                                    )
                                else:
                                    Skill.objects.filter(user=user, id=skill_id).delete()
                            else:
                                Skill.objects.create(user=user, name=skill_data.get('name', ''))

                        # Atualizar os gráficos e tópicos personalizados
                        for custom_data in data.get('Custom', []):

                            # Buscar informações da tabela Graphic
                            if custom_data['topicType']['type'] == 'graphic':
                                custom_id = custom_data.get('id', 0)
                                custom_status = custom_data.get('status', True)

                                # Atualizar tabela Graphic
                                if custom_id > 0:
                                    if custom_status == True:
                                        Graphic.objects.filter(user=user, id=custom_id).update(
                                            title=custom_data.get('title', ''),
                                            description=custom_data.get('description', ''),
                                            percentage=custom_data['topicType'].get('percentage', 0),
                                            color=custom_data['topicType'].get('color', '')
                                        )
                                    else:
                                        Graphic.objects.filter(user=user, id=custom_id).delete()
                                else:
                                    Graphic.objects.create(
                                        user=user,
                                        title=custom_data.get('title', ''),
                                        description=custom_data.get('description', ''),
                                        percentage=custom_data['topicType'].get('percentage', 0),
                                        color=custom_data['topicType'].get('color', '')
                                    )

                            # Buscar informações da table Topic
                            elif custom_data['topicType']['type'] == 'topics':
                                custom_id = custom_data.get('id', 0)
                                custom_status = custom_data.get('status', True)

                                # Atualizar tabela Topic
                                if custom_id > 0:
                                    if custom_status == True:
                                        Topic.objects.filter(user=user, id=custom_id).update(
                                            title=custom_data.get('title', ''),
                                            description=custom_data.get('description', ''),
                                            topics=custom_data['topicType'].get('topics', [])
                                        )
                                    else:
                                        Topic.objects.filter(user=user, id=custom_id).delete()
                                else:
                                    Topic.objects.create(
                                        user=user,
                                        title=custom_data.get('title', ''),
                                        description=custom_data.get('description', ''),
                                        topics=custom_data['topicType'].get('topics', [])
                                    )

                        # Retorne uma resposta de sucesso
                        return JsonResponse({'message': 'Atualizado com sucesso'})
                    
                    else:
                        # Retorne uma resposta de falha
                        return JsonResponse({'error': 'Você não tem permissão para excluir este usuário'}, status=403)
                
                else:
                    # Retorne uma resposta de falha
                    return JsonResponse({'error': 'Dados inválidos'}, status=400)
        
            else:
                # Retorne uma resposta de falha
                return JsonResponse({'error': '"Key" informada não existe'}, status=404)

        except User.DoesNotExist:
            # Retorne uma resposta de falha
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        
        except Exception as e:
            # Em caso de qualquer exceção, retorne uma resposta de erro
            return JsonResponse({'error': str(e)}, status=500)

    # Se não for um request PUT, retorne um erro de método não permitido
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Deletar projeto
@csrf_exempt
def delete_project(request):

    # Informar o metodo
    if request.method == 'DELETE':

        try:

            credential_id = id
            print(f'credential_id: {credential_id}')

            # Buscar a chave do curriculo
            key = request.GET.get('key', None)

            if key:

                # Obtenha o usuário existente
                user = User.objects.get(key=key)

                if user:

                    # Atualize os campos do usuário
                    user_id = str(user.credential_id)
                    print(f'user_id: {user_id}')

                    # Verificar se usuário tem permissão para alterações
                    if user_id == credential_id:
                        user_admin = True
                    else:
                        user_admin = False

                    if user_admin:
            
                        # Exclui todas as entradas relacionadas ao usuário em todas as tabelas
                        Link.objects.filter(user=user).delete()
                        Experience.objects.filter(user=user).delete()
                        Education.objects.filter(user=user).delete()
                        Skill.objects.filter(user=user).delete()
                        Graphic.objects.filter(user=user).delete()
                        Topic.objects.filter(user=user).delete()
                        
                        # Exclui o usuário em si
                        user.delete()
            
                        return JsonResponse({'message': 'Usuário excluído com sucesso'})
                    
                    else:
                        # Retorne uma resposta de falha
                        return JsonResponse({'error': 'Você não tem permissão para excluir este usuário'}, status=403)
                
                else:
                    # Retorne uma resposta de falha
                    return JsonResponse({'error': 'Dados inválidos'}, status=400)
                
            else:
                # Retorne uma resposta de falha
                return JsonResponse({'error': '"Key" informada não existe'}, status=404)

        except User.DoesNotExist:
            # Retorna falha
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        
        except Exception as e:
            # Em caso de qualquer exceção, retorne uma resposta de erro            
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Listar dados do projeto
@csrf_exempt
def list_project(request):

    # Informar o metodo
    if request.method == 'GET':

        try:
            # Obtém o usuário existente pelo ID fornecido na URL
            credential_id = id
            
            # Consulta todos os usuários (currículos)
            users = User.objects.all()

            # Lista para armazenar os currículos formatados
            cvs = []
            my_cvs = []

            # Itera sobre os usuários e formata os dados
            for user in users:
                cv_data = {
                    "name": user.name,
                    "title": user.title,
                    "id": str(user.pk),
                    "key": str(user.key)
                }

                # Verifica se o usuário tem uma chave estrangeira específica
                if user.credential_id == credential_id:
                    my_cvs.append(cv_data)
                else:
                    # Verifica se está publicado
                    if user.published:
                        cvs.append(cv_data)

            # Cria o objeto de resposta com os currículos formatados
            response_data = {
                "cvs": cvs,
                "myCvs": my_cvs
            }

            # Retorna a resposta como JSON
            return JsonResponse(response_data)

        except Exception as e:
            # Em caso de qualquer exceção, retorne uma resposta de erro
            return JsonResponse({'error': str(e)}, status=500)
        
    return JsonResponse({'error': 'Lista não disponivel'}, status=405)