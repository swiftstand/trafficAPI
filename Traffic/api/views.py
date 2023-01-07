from Traffic.models import Updates
from .serializers import UpdateCreateSerializer,AllupdateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from django.utils import timezone
from Traffic.models import Updates


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def createupdate(request):
    data = {}
    print(request.data)
    serializer = UpdateCreateSerializer(data=request.data)
    reco = Updates.objects.all().values_list('recommendations',flat=True)
    print(reco)
    if request.data['recommendations'] == "" or request.data['recommendations'] in reco:
        print("1")
        data['satus']= 'thank you for the information'
    else:
        print("2")
        if serializer.is_valid(raise_exception=True):
            update=serializer.save(request.user)
            data['satus']= 'thank you for the information'
        else:
            data = serializer.errors
            data['status']='fail'
            print(data)
    print(data)
    return Response(data)



@api_view(['GET'])
def getupdates(request, localty):
    now = timezone.now()
    my_list=[]
    count=0
    pop = False
    if request.method == 'GET':
        posts = Updates.objects.filter(localty=localty).order_by('-date_posted')
        serializer = AllupdateSerializer(posts, many=True)
        result= json.loads(json.dumps(serializer.data))
        print(result)
        for i in range(0, len(result)):
            if pop:
                i = i-count
            p=result[i]
            idt=p['id']
            print(p)
            d_post=posts.get(id=idt)
            diff= now - d_post.date_posted
            print(diff)
            print(diff.seconds)
            if diff.seconds <= 172800:
                date=d_post.whenlast()
                result[i]['date_posted']=date
                pop=False
            else:
                result.pop(i)
                pop=True
                count+=1        
        data=result
    return Response(data)