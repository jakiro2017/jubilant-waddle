from django.shortcuts import render
from requests import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import OrganizationSerializer
from .models.organization import Organization
from .error import ErrorCode


class OrgListAPI(viewsets.ModelViewSet):
    queryset = Organization.objects.root_nodes()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Organization.objects.all()
        username = self.request.query_params.get('partner', None)
        if username is not None:
            queryset = queryset.filter(level=1)
        return queryset


class OrgAddAPI(viewsets.ModelViewSet):
    queryset = Organization.objects.root_nodes()
    serializer_class = OrganizationSerializer

    def create(self, request):
        alldata = request.POST
        # desc = alldata.get("desc", "0")
        # name = alldata.get("name", "0")
        desc = request.data.get("desc")
        name = request.data.get("name")
        code = request.data.get("code")
        subpath = request.data.get("subpath")
        try:
            parent = Organization.objects.root_nodes().get()
        except Exception as e:
            print(e.__class__.__name__)
            if e.__class__.__name__ == "DoesNotExist":
                parent = Organization.objects.create(name="BOSS", desc="boss",code="BOSS",subpath="ftech")
            else:
                response_dict = {"c" : ErrorCode.ORG_GENERIC_ERROR,  "m": str(e),
                                 "e" : ErrorCode(ErrorCode.ORG_GENERIC_ERROR.name)}
                return Response(response_dict)

        try:
            Organization.objects.create(name=name, desc=desc, code = code, subpath =subpath, parent=parent)
        except Exception as e:
            response_dict = {"c" : ErrorCode.ORG_GENERIC_ERROR, "m": str(e),
                             "e" : ErrorCode.ORG_GENERIC_ERROR.name}
            return Response(response_dict)

        response_dict = {"result": "true"}
        # update response_dict with whatever you want to send in response
        return Response(response_dict)

    def update(self, request, pk):
        # alldata = request.data
        # desc = alldata.get("desc", "0")
        # name = alldata.get("name", "0")
        desc = request.data.get("desc")
        name = request.data.get("name")
        code = request.data.get("code")
        subpath = request.data.get("subpath")
        try:
            node = Organization.objects.get(pk=pk)
        except Exception as e:
            response_dict = {"c": ErrorCode.ORG_NOT_FOUND, "m": str(e),
                             "e" : ErrorCode.ORG_NOT_FOUND.name}
            return Response(response_dict)
        node.name = name
        node.desc = desc
        node.code = code
        node.subpath = subpath
        try:
            node.save()
        except Exception as e:
            response_dict = {"c": ErrorCode.ORG_GENERIC_ERROR, "m": str(e),
                             "e": ErrorCode.ORG_GENERIC_ERROR.name}
            return Response(response_dict)
        response_dict = {"result": "true"}
        # update response_dict with whatever you want to send in response
        return Response(response_dict)

    def destroy(self, request, pk):
        # alldata = request.data
        # desc = alldata.get("desc", "0")
        # name = alldata.get("name", "0")
        try:
            node = Organization.objects.get(pk=pk)
        except Exception as e:
            response_dict = {"c": ErrorCode.ORG_GENERIC_ERROR, "m": str(e),
                             "e" : ErrorCode.ORG_GENERIC_ERROR.name}
            return Response(response_dict)
        try:
            node.delete()
        except Exception as e:
            response_dict = {"c": ErrorCode.ORG_GENERIC_ERROR, "m": str(e),
                             "e": ErrorCode.ORG_GENERIC_ERROR.name}
            return Response(response_dict)
        response_dict = {"result": "true"}
        # update response_dict with whatever you want to send in response
        return Response(response_dict)
