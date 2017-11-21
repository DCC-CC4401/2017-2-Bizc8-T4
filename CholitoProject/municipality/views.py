import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from complaint.models import Complaint
from CholitoProject.userManager import get_user_index


class IndexView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_complaints_main.html'
    context = {}

    def getComplaintStats(self, complaints):
        stats_complaint = {}
        status_parser = dict(Complaint().COMPLAINT_STATUS)

        for key, value in status_parser.items():
            stats_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = status_parser.get(complaint.status)
            stats_complaint[temp_status] += 1

        return stats_complaint

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        complaints = Complaint.objects.filter(
            municipality=user.municipality)

        self.context['complaints'] = complaints
        self.context['c_user'] = user
        self.context['stats'] = self.getComplaintStats(complaints)
        return render(request, self.template_name, context=self.context)


class StatisticsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_statistics.html'
    context = {}

    def getComplaintStats(self, complaints):
        stats_complaint = {}
        status_parser = dict(Complaint().COMPLAINT_OPTIONS)

        for key, value in status_parser.items():
            stats_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = status_parser.get(complaint.case)
            stats_complaint[temp_status] += 1

        return stats_complaint

    def getComplaintStatsB(self, complaints):
        stats_complaint = {}
        status_parser = dict(Complaint().COMPLAINT_STATUS)

        for key, value in status_parser.items():
            stats_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = status_parser.get(complaint.status)
            stats_complaint[temp_status] += 1

        return stats_complaint

    def filterDate(self, datein, datefin, complaints):
        datein = datein.split("-")
        datefin = datefin.split("-")
        datein= datetime.date(int(datein[0]),int(datein[1]),int(datein[2]))
        datefin = datetime.date(int(datefin[0]), int(datefin[1]), int(datefin[2]))
        complaintsFil = []
        for complaint in complaints:
            if datein <= complaint.date <= datefin:
                complaintsFil.append(complaint)

        return complaintsFil

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        complaints = Complaint.objects.filter(municipality=user.municipality)
        self.context['c_user'] = user
        self.context['stats'] = self.getComplaintStats(complaints)
        self.context['statsb'] = self.getComplaintStatsB(complaints)
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        user = get_user_index(request.user)
        datein = request.POST['in']
        datefin = request.POST['fin']
        if datein=='' or datefin == '':
            print("-----")
            return self.get(request)

        complaints = Complaint.objects.filter(municipality=user.municipality)
        self.context['stats'] = self.getComplaintStats(complaints)

        complaints = self.filterDate(datein, datefin, complaints)
        self.context['c_user'] = user

        self.context['statsb'] = self.getComplaintStatsB(complaints)
        return render(request, self.template_name, context=self.context)


class UserDetail(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        if 'avatar' in request.FILES:
            c_user.municipality.avatar = request.FILES['avatar']
            c_user.municipality.save()
        return redirect('/')
