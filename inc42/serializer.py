from rest_framework import serializers

from .models import Company, Funding


class CompanySerializer(serializers.ModelSerializer):
    """
    CompanySerializer
    """
    class Meta:
        model = Company
        exclude = ['id', 'is_deleted', 'created_at', 'modified_at']

    def to_representation(self, obj):
        """
        overriding default method to get related funds as well 
        """
        serialized_data = super(CompanySerializer, self).to_representation(obj)
        fundings = obj.funding_set.all()
        funding_fields = Funding._meta.fields
        serialized_data['fundings'] = []
        exclude = ['id', 'company']
        for funding in fundings:
            temp = {}
            for funding_field in funding_fields:
                if funding_field.name in exclude:
                    continue
                temp[funding_field.name] = getattr(funding, funding_field.name, '')
            serialized_data['fundings'].append(temp)
        return serialized_data