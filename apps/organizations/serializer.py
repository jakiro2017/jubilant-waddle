# serializers.py
import yaml
import jsonpickle
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models.organization import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    def validate(self,data):
        """
        check that root node must be available
        :param data:
        :return:
        """
        serialized = jsonpickle.encode(data)
        print(yaml.dump(yaml.load(serialized), indent=2))

    def create(self, validated_data):
        name = validated_data.get("name", None)
        serialized = jsonpickle.encode(validated_data)
        print(yaml.dump(yaml.load(serialized), indent=2))
    class Meta:
        model = Organization
        fields = ('id', 'name', 'code' , 'subpath' , 'desc', 'parent_id', 'level', 'children')
