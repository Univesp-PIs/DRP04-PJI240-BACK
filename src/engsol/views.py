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

                # Carregar dados do status
                status_id = timeline_item.get('id', 0)

                if status_id == 0:
                    
                    # Criar novo status
                    status = Status.objects.create(
                        name=timeline_item['name']
                    )

                else:
                    # Atualizar status existente
                    status = Status.objects.get(id=status_id)
                    status.name = timeline_item['name']
                    status.save()

                # Inserir dados do ranking
                Ranking.objects.create(
                    project=project,
                    status=status,
                    rank=timeline_item['rank']
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
    if request.method == 'POST':

        try:

             # Carregar dados do json
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
                status_id = timeline_item.get('id')

                # Verifica se existe status
                if not status_id:

                    # Criar novo status
                    status = Status.objects.create(
                        name=timeline_item['name']
                    )

                else:
                    # Atualizar status existente
                    status = get_object_or_404(Status, id=status_id)
                    status.name = timeline_item['name']
                    status.save()

                # Atualizar ou criar o ranking
                ranking, created = Ranking.objects.get_or_create(
                    project=project,
                    status=status
                )

                ranking.rank = timeline_item['rank']
                ranking.status = timeline_item['status']
                ranking.save()
            
            # Resposta de sucesso
            response_data = {
                'message': 'Projeto atualizado com sucesso'
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


# Listar projeto
@csrf_exempt
def list_project(request, project_id):

    # Definir metodo
    if request.method == 'GET':

        try:

            # Buscar o projeto pelo ID
            project = get_object_or_404(Project, id=project_id)

            # Buscar o cliente associado ao projeto
            client = project.client

            # Buscar o ranking associado ao projeto
            rankings = Ranking.objects.filter(project=project)

            # Cria lista para timeline
            timeline = []

            # Preenche a lista da timeline com dados dos rankings
            for ranking in rankings:
                timeline.append({
                    'id': ranking.status.id,
                    'name': ranking.status.name,
                    'rank': ranking.rank,
                    'last_update': ranking.last_update.strftime('%d/%m/%Y')
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
def delete_project(request, project_id):

    # Definir metodo
    if request.method == 'DELETE':

        try:

            # Buscar o projeto pelo ID e deletar todos os rankings e o projeto
            project = get_object_or_404(Project, id=project_id)

            # Deletar rankings e projeto
            Ranking.objects.filter(project=project).delete()
            project.delete()

            # Resposta de sucesso
            response_data = {
                'message': 'Projeto atualizado com sucesso'
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:

            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
