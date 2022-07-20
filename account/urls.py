from django.urls import path
from . import views

urlpatterns=[
    path('signin', views.signin),
    path('postsign',views.postsign),
    path('logout',views.logout,name='log'),
    path('signup',views.signup,name='signup'),
    path('postsignup',views.postsignup,name='postsignup'),
    path('postadd',views.postadd),
    path('addpostfirst',views.addpostfirst),
    path('cus_home',views.cus_home),
    path('hello',views.hello),
    path('postdetail',views.postdetail),
    # path('addpost/<str:id>',views.addpost),
    path('myads',views.myads),
    path('post_pro',views.post_pro),
    path('update_pro',views.update_pro),

    path('profilesettings',views.profilesettings),
    path('updateprofile',views.updateprofile),
    path('dataup',views.dataup),
    path('productdetails/<key>',views.productdetails),
    path('eval_pro_details/<pid>/<uid>',views.eval_pro_details),
    path('evaluation/<pid>/<uid>',views.evaluation),
    path('evaluator_dash',views.evaluator_dash),
    path('solded_products',views.solded_products),
    path('Inactive_products',views.Inactive_products),
    path('evaluated_products',views.evaluated_products),
    path('evaluator_profile',views.evaluator_profile),





    path('evaluating',views.evaluating),
    path('forgot',views.forgot),
    path('forgotpage',views.forgotpage),
    path('date_show',views.date_show),
    path('product_history',views.product_history),
    path('date_shows',views.date_shows),
    path('product_history_bn',views.product_history_bn),
    path('eval_history',views.eval_history),
    path('date_show_eval',views.date_show_eval),
    path('eval_history_bn',views.eval_history_bn),
    path('rejected_products',views.rejected_products),
    path('ev_active_products',views.ev_active_products),






    path('date_show_eval_bn',views.date_show_eval_bn),
    path('categories_f',views.categories_f),
    # path('addpost_jewel/<jw>',views.addpost_jewel),
    path('addpost/<fr>',views.addpost),
    path('addpost_pic/<pr>/<fr>',views.addpost_pic),
    path('update_pic/<pr>/<fr>',views.update_pic),
    path('update_post/<up>',views.update_post),
    path('delete_pro/<dl>',views.delete_pro),


    path('pro_com/<p>',views.pro_com),
    path('pics_add',views.pics_add),
    path('dem_pro',views.dem_pro),

    path('categories',views.categories),
    path('about',views.about),
    path('all_product',views.all_product),
    path('all_products/<category>',views.all_products),




    path('faq',views.faq),
    path('popular_products',views.popular_products),
    path('featured_products',views.featured_products),
    path('contact',views.contact),
    path('cus_pro_details/<pid>/<uid>',views.cus_pro_details),
    path('coins_check/<pid>/<uid>',views.coins_check),
    path('requests/<rid>',views.requests),
    path('addcoin/<upid>/<apid>/<auid>',views.addcoin),
    path('removecoin/<upid>/<apid>/<auid>',views.removecoin),
    path('requested_products',views.requested_products),
    path('approval',views.approval),
    path('sold_recieved',views.sold_recieved),
    path('approve_click/<chid>',views.approve_click),
    path('reject_click/<chid>',views.reject_click),
    path('satisfied_recieved',views.satisfied_recieved),
    path('satisfied_given',views.satisfied_given),

    path('satisfy_click/<chid>',views.satisfy_click),
    path('nonsatisfy_click/<chid>',views.nonsatisfy_click),
    path('recieved_sold',views.recieved_sold),
    path('search',views.search),
















]