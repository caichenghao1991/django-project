from rest_framework import serializers, viewsets

from mainapp.models import Student, House

class HouseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('name',)

class StudentModelSerializer(serializers.ModelSerializer):
    #house = HouseModelSerializer   # (many=True) if one side   Hyperlinked
    #house = serializers.HyperlinkedRelatedField(view_name='house-detail', read_only=True)
    #house = serializers.HyperlinkedIdentityField(view_name="api:house-detail")
    class Meta:
        model = Student
        fields = ('id', 'name', 'age', 'house','password')

    # def create(self, validated_data):   # don't support house.name, otherwise no need
    #     if no "house = HouseModelSerializer" house will not be serialized and linked
    #     print(validated_data)  #{'name': 'cai', 'age': 11, 'house': {'name': 'Gryffindor'}}
    #     student = Student.objects.create(**validated_data)
    #     return student

class StudentAPIView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

class HouseAPIView(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseModelSerializer