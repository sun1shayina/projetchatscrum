from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from .models import *
from .serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.core import serializers
from django.core.files.storage import FileSystemStorage
import random
import datetime
import re
import json

# Create your views here.

'''
def create_user(request):
    return render(request, "create_user.html")
    
def init_user(request):
    password = request.POST.get('password', None)
    rtpassword = request.POST.get('rtpassword', None)
    if password != rtpassword:
        messages.error(request, 'Error: Passwords Do Not Match.')
        return HttpResponseRedirect(reverse('Scrum:create_user'))
    user, created = User.objects.get_or_create(username=request.POST.get('username', None))
    if created:
        user.set_password(password)
        group = Group.objects.get(name=request.POST.get('usertype', None))
        group.user_set.add(user)
        user.save()
        scrum_user = ScrumUser(user=user, nickname=request.POST.get('full_name'), age=request.POST.get('age', None))
        scrum_user.save()
        messages.success(request, 'User Created Successfully.')
        return HttpResponseRedirect(reverse('Scrum:create_user'))
    else:
        messages.error(request, 'Error: Username Already Exists.')
        return HttpResponseRedirect(reverse('Scrum:create_user'))
        
def scrum_login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    
    login_user = authenticate(request, username=username, password=password)
    if login_user is not None:
        login(request, login_user)
        return HttpResponseRedirect(reverse('Scrum:profile'))
    else:
        messages.error(request, 'Error: Invalid Credentials.')
        return HttpResponseRedirect(reverse('login'))
        
def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        user_info = request.user.scrumuser
        role = request.user.groups.all()[0].name
        goal_list = ScrumGoal.objects.order_by('user__nickname', '-id')
        nums = [x for x in range(4)]
        final_list = []
        item_prev = None
        
        for item in goal_list:
            if item.user != item_prev:
                item_prev = item.user
                final_list.append((item, goal_list.filter(user=item.user).count()))
            else:
                final_list.append((item, 0))
                
        context = {'username': username, 'user_info': user_info, 'role': role, 'goal_list': final_list, 'nums_list': nums}
        return render(request, "profile.html", context)
    else:
        messages.error(request, 'Error: Please login first.')
        return HttpResponseRedirect(reverse('login'))
    
def scrum_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
    
def add_goal(request):
    if request.user.is_authenticated:
        name_goal = request.POST.get('name', None)
        group_name = request.user.groups.all()[0].name
        status_start = 0
        if group_name == 'Admin':
            status_start = 1
        elif group_name == 'Quality Analyst':
            status_start = 2
        goal = ScrumGoal(user=request.user.scrumuser, name=name_goal, status=status_start)
        goal.save()
        messages.success(request, 'Goal Added Successfully.')
        return HttpResponseRedirect(reverse('Scrum:profile'))
    else:
        messages.error(request, 'Error: Please login first.')
        return HttpResponseRedirect(reverse('login'))
        
def remove_goal(request, goal_id):
    if request.user.is_authenticated:
        if request.user.groups.all()[0].name == 'Developer':
            if request.user != ScrumGoal.objects.get(id=goal_id).user.user:
                messages.error(request, 'Permission Denied: Unauthorized Deletion of Goal.')
                return HttpResponseRedirect(reverse('Scrum:profile'))
                
        del_goal = ScrumGoal.objects.get(id=goal_id)
        del_goal.delete()
        messages.success(request, 'Goal Removed Successfully.')
        return HttpResponseRedirect(reverse('Scrum:profile'))
    else:
        messages.error(request, 'Error: Please login first.')
        return HttpResponseRedirect(reverse('login'))
        
def move_goal(request, goal_id, to_id):
    if request.user.is_authenticated:
        goal_item = ScrumGoal.objects.get(id=goal_id)
        group = request.user.groups.all()[0].name
        from_allowed = []
        to_allowed = []
        
        if group == 'Developer':
            if request.user != goal_item.user.user:
                messages.error(request, 'Permission Denied: Unauthorized Movement of Goal.')
                return HttpResponseRedirect(reverse('Scrum:profile'))
        
        if group == 'Owner':
            from_allowed = [0, 1, 2, 3]
            to_allowed = [0, 1, 2, 3]
        elif group == 'Admin':
            from_allowed = [1, 2]
            to_allowed = [1, 2]
        elif group == 'Developer':
            from_allowed = [0, 1]
            to_allowed = [0, 1]
        elif group == 'Quality Analyst':
            from_allowed = [2, 3]
            to_allowed = [2, 3]
            
        if (goal_item.status in from_allowed) and (to_id in to_allowed):
            goal_item.status = to_id
        elif group == 'Quality Analyst' and goal_item.status == 2 and to_id == 0:
            goal_item.status = to_id
        else:
            messages.error(request, 'Permission Denied: Unauthorized Movement of Goal.')
            return HttpResponseRedirect(reverse('Scrum:profile'))
        
        goal_item.save()
        messages.success(request, 'Goal Moved Successfully.')
        return HttpResponseRedirect(reverse('Scrum:profile'))
    else:
        messages.error(request, 'Error: Please login first.')
        return HttpResponseRedirect(reverse('login'))
'''

def createDemoUser(request):
    demo_user = User.objects.create(username='demouser' + str(random.random())[2:])
    demo_user_password = 'demopassword' + str(random.random())[2:]
    demo_user.set_password(demo_user_password)
    demo_user.save()
    
    demo_scrumuser = ScrumUser(user=demo_user, nickname='Demo User')
    demo_scrumuser.save()
    
    demo_project_name = 'Demo Project #' + str(demo_user.pk)
    demo_project = ScrumProject(name=demo_project_name)
    demo_project.save()
    
    demo_projectrole = ScrumProjectRole(role="Owner", user=demo_scrumuser, project=demo_project)
    demo_projectrole.save()
    
    demo_projectdemo = ScrumDemoProject(project=demo_project, expiration_date=datetime.datetime.now() + datetime.timedelta(hours=24))
    demo_projectdemo.save()
    
    return JsonResponse({'username': demo_user.username, 'password': demo_user_password, 'project': demo_project_name})
    
    
class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    
    def create(self, request):
        # Pattern Match For an Email: https://www.regular-expressions.info/email.html
        regex_pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        if regex_pattern.match(request.data['email']) == None:
            return JsonResponse({'message': 'Error: Invalid email specified.'})
        if request.data['usertype'] == 'Owner' and ScrumProject.objects.filter(name__iexact=request.data['projname']).count() > 0:
            return JsonResponse({'message': 'Error: That project name is already taken.'})
        if request.data['usertype'] == 'Owner' and len(request.data['projname']) > 50:
            return JsonResponse({'message': 'Error: A project name cannot go over 50 characters.'})
        if len(request.data['full_name']) > 50:
            return JsonResponse({'message': 'Error: A user nickname cannot go over 50 characters.'})
        
        user, created = User.objects.get_or_create(username=request.data['email'], email=request.data['email'])
        if created:
            scrum_user = ScrumUser(user=user, nickname=request.data['full_name'])
            scrum_user.save()
            if request.data['usertype'] == 'Owner':
                scrum_project = ScrumProject(name=request.data['projname'])
                scrum_project.save()
                scrum_project_role = ScrumProjectRole(role="Owner", user=scrum_user, project=scrum_project)
                scrum_project_role.save()

            user.set_password(request.data['password'])
            user.save()
            return JsonResponse({'message': 'User Created Successfully.'})
        else:
            return JsonResponse({'message': 'Error: User with that e-mail already exists.'})

            
def filtered_users(project_id):
    project = ScrumProjectSerializer(ScrumProject.objects.get(id=project_id)).data
    time_check = datetime.datetime.utcnow().replace(tzinfo=None)
    for user in project['scrumprojectrole_set']:
        user['scrumgoal_set'] = [x for x in user['scrumgoal_set'] if x['visible'] == True]
        total_hours = 0
        
        for goal in user['scrumgoal_set']:
            if (time_check - parse_datetime(goal['time_created']).replace(tzinfo=None)).days < 7:
                if goal['hours'] != -1 and goal['status'] == 3:
                    total_hours += goal['hours']
        
        user['total_week_hours'] = total_hours
            
        
    return project['scrumprojectrole_set']


class ScrumProjectViewSet(viewsets.ModelViewSet):
    queryset = ScrumProject.objects.all()
    serializer_class = ScrumProjectSerializer
    
    def retrieve(self, request, pk=None):
        try:
            queryset = ScrumProject.objects.get(pk=pk)
            return JsonResponse({'project_name': queryset.name, 'data': filtered_users(pk)})
        except ScrumProject.DoesNotExist:
            return JsonResponse({'detail': 'Not found.'})
    
class ScrumProjectRoleViewSet(viewsets.ModelViewSet):
    queryset = ScrumProjectRole.objects.all()
    serializer_class = ScrumProjectRoleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def patch(self, request):
        scrum_project = ScrumProject.objects.get(id=request.data['project_id'])
        scrum_project_role = scrum_project.scrumprojectrole_set.get(user=request.user.scrumuser)
        to_id = request.data['id'][1:]
        
        author = ScrumProjectRole.objects.get(id=to_id)
        author.role = request.data['role'].capitalize()
        if request.data['role'] == 'quality analyst':
            author.role = 'Quality Analyst'
        author.save()
        
        return JsonResponse({'message': 'User Role Changed!', 'data': filtered_users(request.data['project_id'])})

class ScrumGoalViewSet(viewsets.ModelViewSet):
    queryset = ScrumGoal.objects.all()
    serializer_class = ScrumGoalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        user_id = request.data['user'][1:]
        scrum_project = ScrumProject.objects.get(id=request.data['project_id'])
        scrum_project_role = scrum_project.scrumprojectrole_set.get(user=request.user.scrumuser)
        author = ScrumProjectRole.objects.get(id=user_id)
        sprint = ScrumSprint.objects.filter(goal_project_id = request.data['project_id'])
        print("Last sprint end time: " + (datetime.datetime.strftime(ScrumSprint.objects.latest('ends_on').ends_on, "%Y-%m-%d %H:%M:%S")))
        print("Present date: " + str(datetime.datetime.now().replace(tzinfo=None)))
            
        if scrum_project_role != author and scrum_project_role.role != 'Owner': 
            return JsonResponse({'message': 'Permission Denied: Unauthorized Addition of a Goal.', 'data': filtered_users(request.data['project_id'])})
        
        if len(sprint) < 1:
             return JsonResponse({'message': 'Permission Denied: Sprint not yet started.', 'data': filtered_users(request.data['project_id'])})

        if (datetime.datetime.strftime(ScrumSprint.objects.latest('ends_on').ends_on, "%Y-%m-%d %H:%M:%S")) < datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"):
            return JsonResponse({'message': 'Permission Denied: Last Sprint Period Elapsed.', 'data': filtered_users(request.data['project_id'])})

        status_start = 0
        scrum_project.project_count = scrum_project.project_count + 1
        scrum_project.save()
        goal = ScrumGoal(name=request.data['name'], status=status_start, time_created = datetime.datetime.now(), goal_project_id=scrum_project.project_count, user=author, project_id=request.data['project_id'], moveable = True)
        goal.save()
        return JsonResponse({'message': 'Goal Added!', 'data': filtered_users(request.data['project_id'])})
          
    def patch(self, request):
        scrum_project = ScrumProject.objects.get(id=request.data['project_id'])
        scrum_project_a = scrum_project.scrumprojectrole_set.get(user=request.user.scrumuser)
        scrum_project_b = scrum_project.scrumgoal_set.get(goal_project_id=request.data['goal_id'][1:]).user
        goal_id = request.data['goal_id'][1:]
        to_id = int(request.data['to_id'])
        goal_item = scrum_project.scrumgoal_set.get(goal_project_id=goal_id)
        
        if to_id == 4:
            if scrum_project_a.role == 'Developer':
                if request.user != scrum_project_b.user.user:
                    return JsonResponse({'message': 'Permission Denied: Unauthorized Deletion of Goal.', 'data': filtered_users(request.data['project_id'])})
                    
            del_goal = scrum_project.scrumgoal_set.get(goal_project_id=goal_id)
            del_goal.visible = False
            del_goal.save()         
            self.createHistory(goal_item.name, goal_item.status, goal_item.goal_project_id, goal_item.hours, goal_item.time_created, goal_item.user, goal_item.project, goal_item.file, goal_item.id, 'Goal Removed Successfully by')
            return JsonResponse({'message': 'Goal Removed Successfully!', 'data': filtered_users(request.data['project_id'])})
        else:           
            group = scrum_project_a.role
            from_allowed = []
            to_allowed = []
            if group == 'Developer':
                if request.user != scrum_project_b.user.user:
                    return JsonResponse({'message': 'Permission Denied: Unauthorized Movement of Goal.', 'data': filtered_users(request.data['project_id'])})
            
            if group == 'Owner':
                from_allowed = [0, 1, 2, 3]
                to_allowed = [0, 1, 2, 3]
            elif group == 'Admin':
                from_allowed = [0, 1, 2]
                to_allowed = [0, 1, 2]
            elif group == 'Developer':
                from_allowed = [0, 1, 2]
                to_allowed = [0, 1, 2]
            elif group == 'Quality Analyst':
                from_allowed = [0, 1, 2, 3]
                to_allowed = [0, 1, 2, 3]
            
            state_prev = goal_item.status
            
            if (goal_item.status in from_allowed) and (to_id in to_allowed):
                goal_item.status = to_id
            elif group == 'Quality Analyst' and goal_item.status == 2 and to_id == 0:
                goal_item.status = to_id
            elif request.user == scrum_project_b.user.user:
                if goal_item.status == 1 and to_id == 0:
                    goal_item.status = to_id
                elif goal_item.status == 0 and to_id == 1:
                    goal_item.status = to_id
                else:
                    return JsonResponse({'message': 'Permission Denied: Unauthorized Movement of Goal.', 'data': filtered_users(request.data['project_id'])})
            else:
                return JsonResponse({'message': 'Permission Denied: Unauthorized Movement of Goal.', 'data': filtered_users(request.data['project_id'])})
            if goal_item.moveable == True:
                message = 'Goal Moved Successfully!'
                if request.data['hours'] > 8:
                    goal_item.status = state_prev
                    message = 'Error: Task Exceeds 8 hours of completion.'
                elif request.data['hours'] == -1 and goal_item.hours == -1 and to_id > 1:
                     goal_item.status = state_prev
                     message = 'Error: A Task must have hours assigned.'
                elif to_id == 2 :
                    goal_item.hours = request.data['hours']
                    message = 'Goal Moved Successfully! Hours Applied!' 
                self.createHistory(goal_item.name, goal_item.status, goal_item.goal_project_id, goal_item.hours, goal_item.time_created, goal_item.user, goal_item.project, goal_item.file, goal_item.id, 'Goal Moved Successfully by')          
                goal_item.save()
            else:
                message = "Sprint Period Elapsed, The Goal Cannot be Moved!"
            
            return JsonResponse({'message': message, 'data': filtered_users(request.data['project_id'])})
            
    def put(self, request):
        scrum_project = ScrumProject.objects.get(id=request.data['project_id'])
        scrum_project_role = scrum_project.scrumprojectrole_set.get(user=request.user.scrumuser)
        scrum_project_b = scrum_project.scrumgoal_set.get(goal_project_id=request.data['goal_id'][1:]).user
        if request.data['mode'] == 0:
            from_id = request.data['goal_id'][1:]
            to_id = request.data['to_id'][1:]
            
            if scrum_project_role.role == 'Developer' or scrum_project_role.role == 'Quality Analyst':
                return JsonResponse({'message': 'Permission Denied: Unauthorized Reassignment of Goal.', 'data': filtered_users(request.data['project_id'])})
                
            goal = scrum_project.scrumgoal_set.get(goal_project_id=from_id)
            if goal.moveable == True:
            
                author = ScrumProjectRole.objects.get(id=to_id)
                goal.user = author
                self.createHistory(goal.name, goal.status, goal.goal_project_id, goal.hours, goal.time_created, goal.user, goal.project, goal.file, goal.id, 'Goal Reassigned Successfully by')
                goal.save()
                return JsonResponse({'message': 'Goal Reassigned Successfully!', 'data': filtered_users(request.data['project_id'])})
            else:
                return JsonResponse({'message': 'Permission Denied: Sprint Period Elapsed!!!', 'data': filtered_users(request.data['project_id'])})
        elif request.data['mode'] == '1':
            goal = scrum_project.scrumgoal_set.get(goal_project_id=request.data['goal_id'][1:])
            # goal.file = request.FILES['image']
            

            myfile = request.FILES['image']
            fs = FileSystemStorage()
            print(myfile)
            print(myfile.name)
        
            filename = fs.save(myfile.name, myfile)
            goal.file = filename
            self.createHistory(goal.name, goal.status, goal.goal_project_id, goal.hours, goal.time_created, goal.user, goal.project, goal.file, goal.id, 'Image Added Successfully by')
            goal.save()
            
            return JsonResponse({'message': 'Image Added Successfully', 'data': filtered_users(request.data['project_id'])})
        elif request.data['mode'] == 2:
            goal = scrum_project.scrumgoal_set.get(goal_project_id=request.data['goal_id'][1:])
            if request.user == scrum_project_b.user.user and goal.moveable == True:

                goal.visible = 0
                goal.save()
                print(request.user.id)
                return JsonResponse({'message': 'Goal Deleted Successfully!', 'data': filtered_users(request.data['project_id'])})
            else:
                return JsonResponse({'message': 'Permission Denied: Unauthorized Deletion of Goal.', 'data': filtered_users(request.data['project_id'])})
            
        else:
            scrum_project_b = scrum_project.scrumgoal_set.get(goal_project_id=request.data['goal_id'][1:]).user
            if scrum_project_role.role != 'Owner' and request.user != scrum_project_b.user.user:
                return JsonResponse({'message': 'Permission Denied: Unauthorized Name Change of Goal.', 'data': filtered_users(request.data['project_id'])})
            
            goal = scrum_project.scrumgoal_set.get(goal_project_id=request.data['goal_id'][1:])
            if goal.moveable == True:            
                goal.name = request.data['new_name']
                self.createHistory(goal.name, goal.status, goal.goal_project_id, goal.hours, goal.time_created, goal.user, goal.project, goal.file, goal.id,  'Goal Name Changed by')
                goal.save()
                return JsonResponse({'message': 'Goal Name Changed!', 'data': filtered_users(request.data['project_id'])})
            else:
                 return JsonResponse({'message': 'Permission Denied: Sprint Period Elapsed!!!', 'data': filtered_users(request.data['project_id'])})
    def createHistory(self, name, status, goal_project_id, hours, time_created, user, project, file, goal, message):
        concat_message = message + self.request.user.username
        print(concat_message)
        goal = ScrumGoalHistory (name=name, status=status, time_created = time_created, goal_project_id=goal_project_id, user=user, project=project, file=file, goal_id=goal, done_by=self.request.user, message=concat_message)
        goal.save()
        return
            
def jwt_response_payload_handler(token, user=None, request=None):
    project = None
    try:
        project = ScrumProject.objects.get(name__iexact=request.data['project'])
    except ScrumProject.DoesNotExist:
        raise ValidationError('The selected project does not exist.');
    
    if project.scrumprojectrole_set.filter(user=user.scrumuser).count() == 0:
        scrum_project_role = ScrumProjectRole(role="Developer", user=user.scrumuser, project=project)
        scrum_project_role.save()

        
    return {
        'token': token,
        'name': user.scrumuser.nickname,
        'role': project.scrumprojectrole_set.get(user=user.scrumuser).role,
        'project_id': project.id,
        'role_id': project.scrumprojectrole_set.get(user=user.scrumuser).id
    }
    

class SprintViewSet(viewsets.ModelViewSet):
    queryset = ScrumSprint.objects.all()
    serializer_class = ScrumSprintSerializer

    def get_queryset(self):
        queryset = self.get_project_sprint()
        return queryset

    def create(self, request):     
        user_id = request.user.id
        scrum_project = ScrumProject.objects.get(id=request.data['project_id'])
        scrum_project.project_count = scrum_project.project_count + 1
        scrum_project.save()
        # Get the owner of project, the first item.project_id... 
        scrum_project_creator = scrum_project.scrumprojectrole_set.all()[0]

        scrum_project_role = scrum_project.scrumprojectrole_set.get(user=request.user.scrumuser)

        print(user_id)

        author_role = ScrumUser.objects.get(user_id=user_id)
        author = author_role.scrumprojectrole_set .all()

        sprint_goal_carry = ScrumGoal.objects.filter(project_id = request.data['project_id']) 
        

        existence = ScrumSprint.objects.filter(goal_project_id = request.data['project_id']).exists()
        now_time = datetime.datetime.now().replace(tzinfo=None)  + datetime.timedelta(seconds=10)             



        if scrum_project_role.role == 'Admin' or scrum_project_role.role == 'Owner':
            if existence == True:   
                last_sprint = ScrumSprint.objects.latest('ends_on')           
                if (datetime.datetime.strftime(last_sprint.ends_on, "%Y-%m-%d")) < datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"):
                    sprint = ScrumSprint(goal_project_id=request.data['project_id'], created_on = now_time, ends_on=datetime.datetime.now() + datetime.timedelta(days=7))
                    sprint.save()
                    self.change_goal_moveability(sprint_goal_carry, scrum_project, scrum_project_role)
                    queryset = self.get_project_sprint()
                    return JsonResponse({'message': 'Sprint Created Successfully.', 'data':queryset,  'users': filtered_users(request.data['project_id'])})
                else:
                    if (last_sprint.created_on.replace(tzinfo=None) + datetime.timedelta(seconds=20) > now_time):
                        queryset = self.get_project_sprint() 
                        return JsonResponse({'message': 'Not Allowed: Minimum Allowed Sprint Run is 60secs.', 'data':queryset, 'users': filtered_users(request.data['project_id'])})
                    else: 
                        last_sprint.ends_on = datetime.datetime.now()
                        last_sprint.save()
                        sprint = ScrumSprint(goal_project_id=request.data['project_id'], created_on = now_time, ends_on=datetime.datetime.now() + datetime.timedelta(days=7))
                        sprint.save()                    
                        self.change_goal_moveability(sprint_goal_carry, scrum_project, scrum_project_role)
                        queryset = self.get_project_sprint()
                        return JsonResponse({'message': 'Last Sprint Ended and New Sprint Created Successfully.', 'data':queryset, 'users': filtered_users(request.data['project_id'])})  
            else: 
                sprint = ScrumSprint(goal_project_id=request.data['project_id'], created_on = now_time, ends_on=datetime.datetime.now() + datetime.timedelta(days=7))
                sprint.save()
                self.change_goal_moveability(sprint_goal_carry, scrum_project, scrum_project_role)
                print(self.get_project_sprint())
                queryset = self.get_project_sprint()
                return JsonResponse({'message': 'Sprint Created Successfully.', 'data':queryset, 'users': filtered_users(request.data['project_id'])})            

        else:
            return JsonResponse({'message': 'Permission Denied: Unauthorized Permission to Create New Sprint.', 'users': filtered_users(request.data['project_id'])})


    def change_goal_status(self,sprint_goal_carry):
        for each_goal in sprint_goal_carry:
            if each_goal.status == 0:
                each_goal.time_created = datetime.datetime.now()  + datetime.timedelta(seconds=12)
                each_goal.save()         
        return

    def get_project_sprint(self):        
        project_id = self.request.query_params.get('goal_project_id', None)
        if project_id is not None:
            proj_sprint = ScrumSprint.objects.filter(goal_project_id=project_id)
            serializer = ScrumSprintSerializer(proj_sprint, many = True)
            queryset = serializer.data
        return queryset

    def change_goal_moveability(self, sprint_goal_carry, scrum_project, scrum_project_role):
       
        if sprint_goal_carry :
            scrum_project.project_count = scrum_project.project_count
            for each_goal in sprint_goal_carry:
                if each_goal.moveable != False:
                    each_goal.moveable = False
                    each_goal.save()
                    if each_goal.status == 0 and each_goal.visible == 1 :
                        goal = ScrumGoal(
                        name=each_goal.name,
                        status= 0,
                        time_created = datetime.datetime.now() + datetime.timedelta(seconds=10), 
                        goal_project_id=scrum_project.project_count, 
                        user=each_goal.user, 
                        project_id=self.request.data['project_id'],
                        moveable = True)
                        scrum_project.project_count = scrum_project.project_count + 1                        
                        goal.save()
                
            # # Save Total number of project goals
            scrum_project.save()

        else:
            pass  

        return