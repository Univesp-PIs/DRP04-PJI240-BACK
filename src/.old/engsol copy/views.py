from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from account.models import Credential
from .models import Project, Client, Status, Ranking
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
def update_project(request):

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
def list_project(request, project_id):

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

@csrf_exempt
def delete_project(request, project_id):

    # Informar o metodo
    if request.method == 'DELETE':

        try:
            
            # Buscar o projeto pelo ID
            project = get_object_or_404(Project, id=project_id)

            # Deletar todos os rankings associados ao projeto
            Ranking.objects.filter(project_id=project).delete()

            # Deletar o projeto
            project.delete()

            # Resposta de sucesso
            return JsonResponse({'message': 'Projeto e rankings deletados com sucesso'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)