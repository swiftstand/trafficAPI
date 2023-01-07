from rest_framework import serializers
from Traffic.models import Updates


class UpdateCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model= Updates
        fields = ['long','lang','adress', 'localty','recommendations']

    def save(self, user):

        update= Updates(
            long = self.validated_data['long'],
            lang = self.validated_data['lang'],
            adress = self.validated_data['adress'],
            localty = self.validated_data['localty'],
            recommendations = self.validated_data['recommendations'],
        
        )
        update.author_username = user.username
        update.author = user
        update.save()
        
        return update



class AllupdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    adress = serializers.CharField(style={'base_template': 'textarea.html'},required=False,allow_blank=True,max_length=10000)
    localty = serializers.CharField(required=False,allow_blank=True,max_length=100000)
    author_username = serializers.CharField(required=False,allow_blank=True,max_length=100000)
    recommendations = serializers.CharField(style={'base_template': 'textarea.html'},required=False,allow_blank=True,max_length=10000)
    date_posted = serializers.CharField(required=True,allow_blank=True,max_length=200)


