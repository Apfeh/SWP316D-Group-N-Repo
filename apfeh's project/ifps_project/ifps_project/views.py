from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeamMember  # Adjust import based on your app structure

def manage_team(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            try:
                TeamMember.objects.create(
                    claimid=request.POST['claimid'],
                    policyid=request.POST['policyid'],
                    contactNumber=request.POST['contactNumber'],
                    department=request.POST['department'],
                    investigatorName=request.POST['investigatorName']
                )
                messages.success(request, 'Team member added successfully.')
            except Exception as e:
                messages.error(request, f'Error adding team member: {e}')
        elif action == 'update':
            try:
                teamid = request.POST['teamid']
                member = TeamMember.objects.get(teamid=teamid)
                member.claimid = request.POST['claimid']
                member.policyid = request.POST['policyid']
                member.contactNumber = request.POST['contactNumber']
                member.department = request.POST['department']
                member.investigatorName = request.POST['investigatorName']
                member.save()
                messages.success(request, 'Team member updated successfully.')
            except TeamMember.DoesNotExist:
                messages.error(request, 'Team member not found.')
            except Exception as e:
                messages.error(request, f'Error updating team member: {e}')
        elif action == 'delete':
            try:
                teamid = request.POST.get('teamid')
                member = TeamMember.objects.get(teamid=teamid)
                member.delete()
                messages.success(request, 'Team member removed successfully.')
            except TeamMember.DoesNotExist:
                messages.error(request, 'Team member not found.')
            except Exception as e:
                messages.error(request, f'Error removing team member: {e}')
        return redirect('manage_team')
    
    # GET request: Render the template with team members
    team_members = TeamMember.objects.all()
    return render(request, 'fraud_prevention.html', {'team_members': team_members})