# Copyright (c) 2017 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.keystone import OperateTenant

logger = logging.getLogger(__name__)


class ListTenantsView(APIView):
    def get(self, request, vimid):
        vim_info = extsys.get_vim_by_id(vimid)

        data = {}
        data['vimid'] = vim_info['vimId']
        data['vimName'] = vim_info['name']
        data['username'] = vim_info['userName']
        data['password'] = vim_info['password']
        data['url'] = vim_info['url']
        data['project_name'] = vim_info['tenant']

        tenant_instance = OperateTenant.OperateTenant()
        projects = tenant_instance.get_projects(data)

        rsp = {}
        rsp['vimid'] = vim_info['vimId']
        rsp['vimName'] = vim_info['name']
        rsp['tenants'] = []

        for project in projects:
            tenant = {}
            logger.debug("testproject is : ", project)
            tenant['id'] = project['id']
            tenant['name'] = project['name']
            rsp['tenants'].append(tenant)
        return Response(data=rsp, status=status.HTTP_200_OK)
