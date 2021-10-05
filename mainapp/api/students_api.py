from rest_framework import serializers, viewsets

from mainapp.models import Student, House

class HouseModelSerializer(serializers.HyperlinkedModelSerializer):
    #students = serializers.StringRelatedField(many=True)  # change from hyperlink/id to string object
    #students = serializers.PrimaryKeyRelatedField(many=True)  # change from hyperlink to id
    # serializers.HyperlinkedRelatedField default for HyperlinkedModelSerializer
    students = serializers.SlugRelatedField(many=True,queryset=Student.objects.all(),slug_field='name') # read_only=True
        # change from hyperlink to interested field (slug_field), must add read_only=True or provide `queryset` argument
        # ,
    class Meta:
        model = House
        fields = ('name',)
        fields = ('name', 'students')
class StudentModelSerializer(serializers.HyperlinkedModelSerializer):
    #house = HouseModelSerializer(read_only=True)   # (many=True) if one side   this will expend the house object
    #house = serializers.HyperlinkedRelatedField(view_name='house-detail', read_only=True)

    house = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Student
        fields = ('id', 'name', 'age', 'house', 'password')

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