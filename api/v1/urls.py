from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views_accounts, views_articles, views_categories, views_comments, views_reviews
from . import views_notifications

urlpatterns = [
    # Auth
    path('auth/register/', views_accounts.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', views_accounts.LogoutView.as_view(), name='logout'),

    # Users
    path('users/me/', views_accounts.ProfileView.as_view(), name='profile'),
    path('users/<str:username>/', views_accounts.UserDetailView.as_view(), name='user_detail'),
    path('users/<str:username>/follow/', views_accounts.FollowView.as_view(), name='follow'),

    # Articles
    path('articles/', views_articles.ArticleListView.as_view(), name='article_list'),
    path('articles/my/', views_articles.MyArticlesView.as_view(), name='my_articles'),
    path('articles/<slug:slug>/', views_articles.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<slug:slug>/like/', views_articles.ArticleLikeView.as_view(), name='article_like'),
    path('articles/<slug:slug>/comments/', views_comments.CommentListView.as_view(), name='comment_list'),
    path('articles/<slug:slug>/reviews/', views_reviews.ReviewListView.as_view(), name='review_list'),

    # Comments
    path('comments/<int:pk>/', views_comments.CommentDetailView.as_view(), name='comment_detail'),
    path('comments/<int:pk>/like/', views_comments.CommentLikeView.as_view(), name='comment_like'),

    # Reviews
    path('reviews/<int:pk>/', views_reviews.ReviewDetailView.as_view(), name='review_detail'),

    # Categories
    path('categories/', views_categories.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views_categories.CategoryDetailView.as_view(), name='category_detail'),
   #verify
    path('auth/verify-email/<uidb64>/<token>/', views_accounts.VerifyEmailView.as_view(), name='verify_email'),
    path('auth/resend-verification/', views_accounts.ResendVerificationView.as_view(), name='resend_verification'),
    path('auth/forgot-password/', views_accounts.ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/<uidb64>/<token>/', views_accounts.ResetPasswordView.as_view(), name='reset_password'),

    # Notifications
path('notifications/', views_notifications.NotificationListView.as_view(), name='notification_list'),
path('notifications/unread/', views_notifications.UnreadCountView.as_view(), name='unread_count'),
path('notifications/mark-all-read/', views_notifications.NotificationMarkAllReadView.as_view(), name='mark_all_read'),
path('notifications/<int:pk>/read/', views_notifications.NotificationMarkReadView.as_view(), name='mark_read'),
]