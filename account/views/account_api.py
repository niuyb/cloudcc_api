from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from crm_api.config import ACCOUNT_QUERY_ALLOW, RESULT, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ClOUDCC_OBJECT, \
    ACCOUNT_MODIFY_ALLOW, ACCOUNT_MAPPING
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql, modify_by_api
from public.utils import Result


class account_api(View):
    def get(self,request):
        """
        :param request: field_name,field_value
        :return: data [{},{}]
        """
        result = Result()
        field_name = request.GET.get("field_name",None)
        field_value = request.GET.get("field_value",None)
        if field_name in ACCOUNT_QUERY_ALLOW:
            try:
                access_url=cloudcc_get_request_url(ACCESS_URL,ClOUDCC_USERNAME)
                binding=cloudcc_get_binding(access_url,ClOUDCC_USERNAME,ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                return JsonResponse(result.dict())
            try:
                cloudcc_object = ClOUDCC_OBJECT.get("account")
                sql = """ select id,`name` from `{}` where `{}` like '%{}%' """.format(cloudcc_object,field_name,field_value)
                data =cloudcc_query_sql(access_url,"cqlQuery", cloudcc_object, sql, binding)
                result.data = data
                result.code = 1
            except:
                result.msg = "获取data失败,请检查参数"
                return JsonResponse(result.dict())
        else:
            result.msg = "field_name传参有误,请使用id或name"
        return JsonResponse(result.dict())

    def post(self,request):
        """
        :param request:
        :return: True or False
        """
        result = Result()
        result.msg = "暂不支持新增"
        return JsonResponse(result.dict())

    def put(self,request):
        """
        :param request:  account_id,modify_field,mofidy_value
        :return:  True or False
        """
        result = Result()
        account_id = request.GET.get("account_id",None)
        modify_field = request.GET.get("modify_field",None)
        mofidy_value = request.GET.get("mofidy_value",None)
        print(modify_field)
        if modify_field in ACCOUNT_MODIFY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                return JsonResponse(result.dict())

            try:
                cloudcc_field = ACCOUNT_MAPPING.get(modify_field)
                cloudcc_object = ClOUDCC_OBJECT.get("account")
                data = [{"id":account_id,cloudcc_field:mofidy_value}]
                res_data = modify_by_api(access_url, "update", cloudcc_object, data, binding)
                result.data = res_data
                result.code = 1
            except:
                result.msg = "获取data失败,请检查参数"
                return JsonResponse(result.dict())

        else:
            result.msg = "put modify_field传参有误"

        return JsonResponse(result.dict())


    def delete(self,request):
        """
        :param request: account_id
        :return: True or False
        """
        result = Result()
        result.msg = "暂不支持删除"
        return JsonResponse(result.dict())