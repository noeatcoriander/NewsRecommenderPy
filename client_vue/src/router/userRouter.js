//前台用户路由地址配置文件
//参数unRequiresAuth：即不需要登录权限验证即可路由导航
//参数parentMenu：标记选中的菜单路由地址
const userRouter = [
  {
    path: '/login', component: () => import('@/views/user/public/LoginView.vue'),
    meta: { title: '用户登录', unRequiresAuth: true }
  },
  {
    path: '/register', component: () => import('@/views/user/public/RegisterView.vue'),
    meta: { title: '用户注册', unRequiresAuth: true }
  },
  {
    path: '/forgetPassword', component: () => import('@/views/user/public/ForgetPasswordView.vue'),
    meta: { title: '忘记密码', unRequiresAuth: true }
  },
  {
    path: '/', component: () => import('@/views/user/MainView.vue'),
    children: [
      {
        path: '', component: () => import('@/views/user/index/IndexView.vue'),
        meta: { title: '首页', unRequiresAuth: true }
      },
      {
        path: 'user/news/list', component: () => import('@/views/user/news/ListView.vue'),
        meta: { title: '新闻分类', unRequiresAuth: true }
      },
      {
        path: 'user/news/detail', component: () => import('@/views/user/news/DetailView.vue'),
        meta: { title: '新闻详情', unRequiresAuth: true }
      },
      {
        path: '/user/user/detail', component: () => import('@/views/user/user/DetailView.vue'),
        meta: { title: '个人信息' }
      },
      {
        path: '/user/user/update', component: () => import('@/views/user/user/UpdateView.vue'),
        meta: { title: '修改信息', parentMenu: '/user/user/detail' }
      },
      {
        path: '/user/user/updatePassword', component: () => import('@/views/user/user/UpdatePasswordView.vue'),
        meta: { title: '修改密码', parentMenu: '/user/user/detail' }
      },
      {
        path: '/user/userlabel/update', component: () => import('@/views/user/userlabel/UpdateView.vue'),
        meta: { title: '兴趣标签' }
      },
      {
        path: '/user/userlike/list', component: () => import('@/views/user/userlike/ListView.vue'),
        meta: { title: '我的点赞' }
      },
      {
        path: '/user/userfavor/list', component: () => import('@/views/user/userfavor/ListView.vue'),
        meta: { title: '我的收藏' }
      },
      {
        path: '/user/userscore/list', component: () => import('@/views/user/userscore/ListView.vue'),
        meta: { title: '我的评分' }
      },
      {
        path: '/user/userreview/list', component: () => import('@/views/user/userreview/ListView.vue'),
        meta: { title: '我的评论' }
      },
      {
        path: '/user/userreview/detail', component: () => import('@/views/user/userreview/DetailView.vue'),
        meta: { title: '查看评论', parentMenu: '/user/userreview/list' }
      },
      {
        path: '/user/userreview/update', component: () => import('@/views/user/userreview/UpdateView.vue'),
        meta: { title: '修改评论', parentMenu: '/user/userreview/list' }
      },
      {
        path: '/user/userbrowse/list', component: () => import('@/views/user/userbrowse/ListView.vue'),
        meta: { title: '浏览历史' }
      }
    ]
  }
]

export default userRouter