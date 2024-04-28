from rest_framework import serializers
from .models import company,employee

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ['id','name','email','address','phone_no','position','salary','join_date','company']

        def validate(self,data):
            if employee.objects.filter(email=data['email'].exists):
                return serializers.ValidationError('an employee with this mail already exist ')
            return(data)

###################### other method ############
# class CompanySerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=200)
#     location = serializers.CharField(max_length=100)
#     about = serializers.TextField()
#     type = serializers.CharField(max_length=50,choices=(('IT','IT'),('NON IT','NON IT'),('PHONE NO','PHONE NO')))
#     added_Date= serializers.DateField(auto_now=True)
#     active = serializers.BooleanField(default=True) 

#     def create(self,Validated_date):
#         return company.objects.create(**validated_data) #(**validated_data)  unpack the dictionary and pass its contents as keyword arguments to the create method.
#                                                         # key-value pair in the dictionary is treated as a separate keyword argument, where the key becomes the parameter name and the value becomes the corresponding argument value.

#     def update (self,instance,validated_date):
#         instance.company_id = validated_date.get('company_id',instance.company_id)
#         instance.name = validated_date.get('name',instance.name)
#         instance.location = validated_date.get('location',instance.location)
#         instance.about = validated_date.get('about',instance.about)
#         instance.type = validated_date.get('type',instance.type)
#         instance.added_Date = validated_date.get('added_Date',instance.added_Date)
#         instance.active = validated_date.get('active',instance.active)
#         instance.save()
#         return instance
