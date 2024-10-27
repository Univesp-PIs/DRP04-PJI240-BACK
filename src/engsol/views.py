from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from account.models import Credential

from .models import Project, Client, Condition, Ranking
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

import json

# Criar novo projeto
@csrf_exempt
def create_project(request):

    # Definir metodo
    if request.method == 'POST':

        try:

            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Carregar dados das repartições do json
            project_data = data['project']
            client_data = data['client']
            timeline = data['timeline']

            # Inserir dados do cliente
            client = Client.objects.create(
                name=client_data['name'],
                email=client_data['email']
            )

            # Inserir dados do projeto
            project = Project.objects.create(
                name=project_data['name'],
                key=get_random_string(length=20),
                client=client
            )

            # Criar status e rankings na timeline
            for timeline_item in timeline:

                # Obter dados por itens
                ranking_data = timeline_item['ranking']
                condition_data = timeline_item['condition']

                # Carregar dados do status
                condition_id = condition_data.get('id', 0)
                ranking_id = ranking_data.get('id', 0)

                # Verificar se a condição já existe ou precisa ser criada
                if condition_id == 0:
                    
                    # Criar novo condition
                    condition = Condition.objects.create(
                        name=condition_data['name']
                    )

                else:

                    # Obter a condição
                    condition = Condition.objects.get(pk=condition_id)

                # Verificar se o ranking já existe ou precisa ser criado
                if ranking_id == 0:

                    # Criar novo ranking
                    ranking = Ranking.objects.create(
                        project=project,
                        condition=condition,
                        rank=ranking_data['rank'],
                        last_update=ranking_data.get('last_update', None),
                        note=ranking_data['note'],
                        description=ranking_data.get('description', None)
                    )

            # Resposta de sucesso
            response_data = {
                'message': 'Projeto criado com sucesso'
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


# Atualizar projeto
@csrf_exempt
def update_project(request):

    # Definir metodo
    if request.method == 'PUT':

        try:

            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Carregar dados das repartições do json
            project_data = data['project']
            client_data = data['client']
            timeline = data['timeline']

            # Atualizar projeto
            project = get_object_or_404(Project, id=project_data['id'])
            project.name = project_data['name']
            project.save()

            # Atualizar cliente
            client = get_object_or_404(Client, id=client_data['id'])
            client.name = client_data['name']
            client.email = client_data['email']
            client.save()

            # Atualizar ou criar status e rankings na timeline
            for timeline_item in timeline:

                # Obter dados por itens
                ranking_data = timeline_item['ranking']
                condition_data = timeline_item['condition']

                # Carregar dados do status
                condition_id = condition_data.get('id', 0)
                ranking_id = ranking_data.get('id', 0)

                # Verificar se a condição já existe ou precisa ser criada
                if condition_id == 0:
                    
                    # Criar novo condition
                    condition = Condition.objects.create(
                        name=condition_data['name']
                    )

                else:

                    # Atualizar condition existente
                    condition = get_object_or_404(Condition, id=condition_id)
                    #condition.name = condition_data['name']
                    condition.save()

                # Verificar se o ranking já existe ou precisa ser criado
                if ranking_data['id'] == 0:

                    # Criar novo ranking
                    ranking = Ranking.objects.create(
                        project=project,
                        condition=condition,
                        rank=ranking_data['rank'],
                        last_update=ranking_data.get('last_update', None),
                        note=ranking_data['note'],
                        description=ranking_data.get('description', None)
                    )

                else:

                    # Atualizar ranking existente
                    ranking = get_object_or_404(Ranking, id=ranking_id)
                    ranking.condition = condition
                    ranking.rank = ranking_data['rank']
                    ranking.last_update = ranking_data['last_update']
                    ranking.note = ranking_data['note']
                    ranking.description = ranking_data.get('description', None)
                    ranking.save()

            response_data = {'message': 'Projeto atualizado com sucesso'}
            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


# Informações do projeto
@csrf_exempt
def info_project(request):

    # Definir metodo
    if request.method == 'GET':

        try:

            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Buscar o projeto pelo ID
            project = get_object_or_404(Project, id=data['id'])

            # Buscar o cliente associado ao projeto
            client = project.client

            # Buscar o ranking associado ao projeto
            rankings = Ranking.objects.filter(project=project)

            # Cria lista para timeline
            timeline = []

            # Preenche a lista da timeline com dados dos rankings
            for ranking in rankings:

                # Adiciona dados ao timeline
                timeline.append({
                    'ranking': {
                        'id': ranking.id,
                        'rank': ranking.rank,
                        'last_update': ranking.last_update.strftime('%d/%m/%Y') if ranking.last_update else None,
                        'note': ranking.note,
                        'description': ranking.description
                    },
                    'condition': {
                        'id': ranking.condition.id,
                        'name': ranking.condition.name
                    }
                })

            # Montar o objeto de resposta com dados do projeto, cliente e timeline
            response_data = {
                'project': {
                    'id': project.id,
                    'name': project.name,
                    'key': project.key
                },
                'client': {
                    'id': client.id,
                    'name': client.name,
                    'email': client.email
                },
                'timeline': timeline
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


# Deletar projeto
@csrf_exempt
def delete_project(request):

    # Definir metodo
    if request.method == 'DELETE':

        try:

            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Buscar o projeto pelo ID
            project = get_object_or_404(Project, id=data['id'])

            # Deletar rankings e projeto
            project.delete()

            # Resposta de sucesso
            response_data = {
                'message': 'Projeto deletado com sucesso'
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:

            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Listar todos os projetos
@csrf_exempt
def list_project(request):

    # Verificar se o método é GET
    if request.method == 'GET':

        try:

            # Buscar todos os projetos
            projects = Project.objects.all()

            # Buscar o ranking associado ao projeto
            rankings = Ranking.objects.filter(project=project)

            # Criar uma lista para armazenar os dados dos projetos
            project_list = []
            timeline = []
            
            # Iterar sobre cada projeto e montar o JSON de resposta
            for project in projects:

                # Preenche a lista da timeline com dados dos rankings
                for ranking in rankings:

                    # Adiciona dados ao timeline
                    timeline.append({
                        'ranking': {
                            'id': ranking.id,
                            'rank': ranking.rank,
                            'last_update': ranking.last_update.strftime('%d/%m/%Y') if ranking.last_update else None,
                            'note': ranking.note,
                            'description': ranking.description
                        },
                        'condition': {
                            'id': ranking.condition.id,
                            'name': ranking.condition.name
                        }
                    })

                # Montar o objeto de resposta com dados do projeto, cliente e timeline
                project_data = {
                    'project': {
                        'id': project.id,
                        'name': project.name,
                        'key': project.key
                    },
                    'client': {
                        'id': project.client.id,
                        'name': project.client.name,
                        'email': project.client.email
                    },
                    'timeline': timeline
                }

                # Limpar timeline para o próximo projeto
                project_list.append(project_data)

            # Retornar a lista de projetos em formato JSON
            return JsonResponse(project_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# --------------------------------------------------------------- CONDITION ---------------------------------------------------------------

# Create Condition
@csrf_exempt
def create_condition(request):

    # Verificar se o método é POST
    if request.method == 'POST':

        try:

            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Criar uma nova condição
            condition = Condition.objects.create(
                name=data['name']
            )

            # Resposta de sucesso
            response_data = {
                'message': 'Condição criada com sucesso',
                'condition': {
                    'id': condition.id,
                    'name': condition.name
                }
            }

            return JsonResponse(response_data, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Update Condition
@csrf_exempt
def update_condition(request):

    # Verificar se o método é PUT
    if request.method == 'PUT':

        try:
            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Buscar a condição pelo ID
            condition = get_object_or_404(Condition, id=data['id'])

            # Atualizar os dados da condição
            condition.name = data['name']
            condition.save()

            # Resposta de sucesso
            response_data = {
                'message': 'Condição atualizada com sucesso',
                'condition': {
                    'id': condition.id,
                    'name': condition.name
                }
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Delete Condition
@csrf_exempt
def delete_condition(request):

    # Verificar se o método é DELETE
    if request.method == 'DELETE':

        try:

            # Carregar dados do json
            data = json.loads(request.body.decode('utf-8'))

            # Buscar a condição pelo ID
            condition = get_object_or_404(Condition, id=data['id'])

            # Deletar a condição
            condition.delete()

            # Resposta de sucesso
            response_data = {
                'message': 'Condição deletada com sucesso'
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# List Condition
@csrf_exempt
def list_condition(request):

    # Verificar se o método é GET
    if request.method == 'GET':

        try:

            # Buscar todas as condições
            conditions = Condition.objects.all()

            # Criar uma lista para armazenar os dados das condições
            condition_list = []

            # Iterar sobre cada condição e montar o JSON de resposta
            for condition in conditions:
                condition_data = {
                    'id': condition.id,
                    'name': condition.name
                }
                condition_list.append(condition_data)

            # Retornar a lista de condições em formato JSON
            return JsonResponse(condition_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
