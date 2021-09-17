from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import *
from .model_loader import Mloader
from .generate_js import GetJs
import json
import cloudpickle

#一些全局变量
FILEROOT = 'interact/'
FILEROOTBACK = 'interact\\'


def index(request):
    #可以通过request.user_agent.is_mobile判断是否为移动端访问，从而使用不同模板
    #取session
    user_id = request.session.get('user_id')
    if user_id != None:
        #如果已经登录，则会在cookie里面记录user_id
        user = User.objects.get(id=user_id)
        username = user.name
        account = user.account
        user_info = 'Name:' + str(username)
        has_login = True
    else:
        user_info = 'Guest'
        has_login = False

    return render(request, FILEROOT+'index.html', {
        'user_info': user_info, 'has_login': has_login
    })


def register(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        name = request.POST.get('name')
        all_users = User.objects.all()
        same_account = False
        for user in all_users:
            if account == user.account:
                same_account = True
                break
        if same_account:
            messages.info(request, 'This account has been taken!')
            return redirect('register')
        else:
            try:
                user = User.create_user(account, password, name)
                explore = Explore.init_explore(account, name)
            except:
                messages.info(request, 'Invalid format!')
                return redirect('register')
            else:
                request.session['user_id'] = user.id
                return redirect('dataset')
    else:
        return render(request, FILEROOT+'register.html')


def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        all_users = User.objects.all()
        valid_account = False
        valid_pwd = False
        for user in all_users:
            if account == user.account:
                valid_account = True
                break
        if valid_account:
            for user in all_users:
                if password == user.password:
                    valid_pwd = True
                    request.session['user_id'] = user.id
                    break
            if valid_pwd:
                return redirect('dataset')
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        return render(request, FILEROOT+"login.html")


def dataset(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    all_databases = Database.objects.all()
    db_intros = {}
    max_attr_num = 3
    for db in all_databases:
        db_intro = db.intro
        dis_num = len(db_intro['attrs']['discrete'])
        con_num = len(db_intro['attrs']['continuous'])
        if dis_num > max_attr_num:
            db_intro['attrs']['discrete'] = db_intro['attrs']['discrete'][:max_attr_num]
            db_intro['attrs']['discrete'].append('......')
        if con_num > max_attr_num:
            db_intro['attrs']['continuous'] = db_intro['attrs']['continuous'][:max_attr_num]
            db_intro['attrs']['continuous'].append('......')
        #attr num
        db_intro['attr_num']={'discrete':dis_num,'continuous':con_num}
        db_intros[db.name] = db_intro
    print(db_intros)
    return render(request, FILEROOT+'dataset.html', {'datasets': db_intros})


def dataattr(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    all_databases = Database.objects.all()
    all_db_names = [db.name for db in all_databases]
    try:
        db_name = request.GET['name']
        if db_name not in all_db_names:
            messages.info(request, 'Invalid argument!')
            return redirect('dataset')
        name_valid = False
        for db in all_databases:
            if db_name == db.name:
                request.session['db_id'] = db.id
                name_valid = True
                break
        if not name_valid:
            messages.info(request, 'Invalid argument!')
            return redirect('dataset')
    except:
        try:
            db_id = request.session.get('db_id')
            db = Database.objects.get(id=db_id)
        except:
            messages.info(request, 'Invalid argument!')
            return redirect('dataset')
    db_intro = db.intro
    attr_details = db_intro['attr_details']
    #generate graph js code using attr details 
    attr_contents = {}
    for dis_attr,content in attr_details['discrete'].items():
        attr_content = {'element_id':dis_attr+'_graph'}
        GETJS = GetJs(attr_details['discrete'][dis_attr],'discrete')
        attr_content['js'],is_small = GETJS.generate_random(attr_content['element_id'])
        attr_content['bootstrap_size'] = 4 if is_small else 6
        attr_contents[dis_attr] = attr_content
    for con_attr,content in attr_details['continuous'].items():
        attr_content = {'element_id':con_attr+'_graph'}
        GETJS = GetJs(attr_details['continuous'][con_attr],'continuous')
        attr_content['js'],is_small = GETJS.generate_random(attr_content['element_id'])
        attr_content['bootstrap_size'] = 4 if is_small else 6
        attr_contents[con_attr] = attr_content
    #json.dump(attr_contents,open('D:\\Explore\\test.json','w'))
    return render(request, FILEROOT+"dataattr.html", {'attr_contents': attr_contents})


def models(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    if request.method == 'POST':
        selected_attrs = request.POST.getlist('interest')  # 接受用户选择的喜好，传给模型
        db_id = request.session.get('db_id')
        db = Database.objects.get(id=db_id)

        if(len(selected_attrs) == 0):  # 列表为空
            messages.info(request, 'Select something pls!')
            return redirect('dataattr')

        request.session['selected_attrs'] = selected_attrs
        return redirect('dataattr')
    else:
        try:
            selected_attrs = request.session.get('selected_attrs')
            db_id = request.session.get('db_id')
            db = Database.objects.get(id=db_id)
        except:
            return redirect('dataattr')
    #选择模型
    model_dict = db.trained_models
    return render(request, FILEROOT+"models.html", {'model_dict': model_dict})


def mark(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    try:
        model_name = request.GET['name']
    except:
        try:
            model_name = request.session.get('model_name')
        except:
            messages.info(request, 'unknown model!')
            return redirect('models')

    db_id = request.session.get('db_id')
    db = Database.objects.get(id=db_id)
    trained_models = db.trained_models
        
    if model_name not in list(trained_models.keys()):
        messages.info(request, 'unknown model!')
        return redirect('models')

    request.session['model_name'] = model_name

    data_num = 5
    request.session['mark_data_len'] = data_num
    selected_attrs = request.session.get('selected_attrs')
    print(selected_attrs)
    #加载模型
    model = Mloader(FILEROOT+db.name+'/'+trained_models[model_name]['path'])
    #request.session['model'] = cloudpickle.dumps(model)
    generated_data = model.generate(data_num)
    #print(generated_data)
    selected_data = []
    for i in range(data_num):
        data_dict = {}
        dsc_data = generated_data[i]['discrete']
        ctn_data = generated_data[i]['continuous']
        for attr in selected_attrs:
            if attr in dsc_data.keys():
                data_dict[attr] = dsc_data[attr]
            else:
                data_dict[attr] = ctn_data[attr]
        selected_data.append(data_dict)
    #print(selected_data)
    return render(request, FILEROOT+"mark.html", {'selected_data': selected_data})


def feedback(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    if request.method == 'POST':
        mark_result = []
        # 接受用户的标记
        for i in range(request.session.get('mark_data_len')):
            mark = True if request.POST.get('mark_%d'%(i+1))=='True' else False
            mark_result.append(mark)
        print(mark_result)
        request.session['mark_result'] = mark_result
        return redirect('mark')
    else:
        try:
            mark_result = request.session.get('mark_result')
            print(mark_result)
        except:
            return redirect('mark')
    #选择模型
    return render(request, FILEROOT+"feedback.html", {'mark_result': mark_result})
    

def quit(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('index')

    logout(request)
    return redirect('index')