from rest_framework import serializers
from .models import *

class ScrumGoalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumGoalHistory
        fields = ('id', 'name', 'status', 'goal_project_id', 'hours', 'time_created', 'user', 'project', 'file', 'goal', 'done_by', 'message')
        
class ScrumGoalSerializer(serializers.ModelSerializer):
    scrumgoalhistory_set = ScrumGoalHistorySerializer(many=True)
    class Meta:
        model = ScrumGoal
        fields = ('visible', 'id', 'name', 'status', 'goal_project_id', 'hours', 'time_created', 'user', 'project', 'file', 'scrumgoalhistory_set')
        
class ScrumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumUser
        fields = ('nickname', 'id')

class ScrumSprintSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScrumSprint
        fields = ('id', 'created_on', 'ends_on', 'goal_project_id')
        
class ScrumProjectRoleSerializer(serializers.ModelSerializer):
    user = ScrumUserSerializer()
    scrumgoal_set = ScrumGoalSerializer(many=True)
    
    class Meta:
        model = ScrumProjectRole
        fields = ('role', 'user', 'id', 'scrumgoal_set')        
        
class ScrumProjectSerializer(serializers.HyperlinkedModelSerializer):
    scrumprojectrole_set = ScrumProjectRoleSerializer(many=True)
    class Meta:
        model = ScrumProject
        fields = ('name', 'id', 'scrumprojectrole_set', 'project_count')

