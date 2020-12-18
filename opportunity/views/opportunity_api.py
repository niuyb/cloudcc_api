from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from crm_api.config import OPPORTUNITY_QUERY_ALLOW, RESULT, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ClOUDCC_OBJECT
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import Result


class opportunity_api(View):
    def get(self,request):
        """
        :param request: field_name,field_value,token
        :return: data [{},{}]
        """
        result = Result()
        field_name = request.GET.get("field_name",None)
        field_value = request.GET.get("field_value",None)
        if field_name in OPPORTUNITY_QUERY_ALLOW:
            try:
                access_url=cloudcc_get_request_url(ACCESS_URL,ClOUDCC_USERNAME)
                binding=cloudcc_get_binding(access_url,ClOUDCC_USERNAME,ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                return JsonResponse(result.dict())
            try:
                cloudcc_object = ClOUDCC_OBJECT.get("opportunity")
                sql = """ select id,`name`,`khmc` as accountId from `{}` where `{}` like '%{}%' """.format(cloudcc_object,field_name,field_value)
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
        :param request:  opportunity_id,modify_field,mofidy_value
        :return:  True or False
        """
        result = Result()
        result.msg = "暂不支持修改"
        return JsonResponse(result.dict())


    def delete(self,request):
        """
        :param request: opportunity_id
        :return: True or False
        """
        result = Result()
        result.msg = "暂不支持删除"
        return JsonResponse(result.dict())
