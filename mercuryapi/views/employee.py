"""View module for handling requests about events"""
from mercuryapi.models.department import Department
from django.contrib.auth.models import User #pylint:disable=(imported-auth-user) 
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from mercuryapi.models import Employee



class EmployeeView(ViewSet):
    """mercury employees"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized employee instance
        """
        employee = Employee.objects.get(user=request.auth.user)

        employee = Employee()
        employee.position = request.data["position"]
        employee.dateHired = request.data["dateHired"]
        employee.monthlySales = request.data["monthlySales"]

        department = Department.objects.get(pk=request.data["department"])
        employee.department = department

        try:
            employee.save()
            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single employee
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an employee
        Returns:
            Response -- Empty body with 204 status code
        """

        employee = Employee.objects.get(pk=pk)
        employee.position = request.data["position"]
        employee.dateHired = request.data["dateHired"]
        employee.monthlySales = request.date["monthlySales"]

        department = Department.objects.get(pk=request.data["departmentId"])
        employee.department = department
        employee.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource
        Returns:
            Response -- JSON serialized list of events
        """
        # Get the current authenticated user
        user = User.objects.get(user=request.auth.user)
        employees = Employee.objects.all()

        # Set the `joined` property on every employee
        for employee in employees:
            # Check to see if the gamer is in the attendees list on the employee
            employee.joined = department in employee.departments.all()

        # Support filtering events by game
        department = self.request.query_params.get('departmentId', None)
        if department is not None:
            employees = employees.filter(department__id=type)

        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})
        return Response(serializer.data)
     
    
class EmployeeUserSerializer(serializers.ModelSerializer):
    """JSON serializer for employee host's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DepartmentEmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employee host"""
    user = EmployeeUserSerializer(many=False)

    class Meta:
        model = Department
        fields = ['name']

    class DepartmentSerializer(serializers.ModelSerializer):
        """JSON serializer for games"""
        class Meta:
            model = Department
            fields = ('id', 'name')

class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    department = DepartmentEmployeeSerializer(many=False)
    

    class Meta:
        model = Employee
        fields = ('id', 'position',
                  'dateHired', 'monthlySales', 'department')