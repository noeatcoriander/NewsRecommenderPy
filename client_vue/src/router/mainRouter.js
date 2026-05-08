/**
 * vue3前端系统全局router路由器配置
 * router路由器用于实现前端页面跳转
 */
import { createRouter, createWebHistory } from 'vue-router'
import userRouter from './userRouter'
import { ElMessage } from "element-plus"
import { projectNameGlobal } from "@/tool/public"
import { useUserStore } from "@/store/userStore"

//创建全局router路由器实例对象
const router = createRouter({
  //配置路由模式：历史模式
  history: createWebHistory(import.meta.env.BASE_URL),
  //配置路由地址
  routes: [
    ...userRouter, //前台用户路由地址
    //404路由地址
    { path: '/:pathMatch(.*)*', meta: { title: '页面不存在' }, component: () => import('@/views/public/404.vue') }
  ]
})

/**
 * 全局前置路由守卫配置
 * 该守卫在页面跳转前执行，用于权限验证、网页标签标题修改等
 * to: 即将进入的路由对象（目标页面路由）
 * from: 当前导航正要离开的路由对象（当前页面路由）
 * next: 钩子函数，决定路由是否继续导航，即页面是否继续跳转
 */
router.beforeEach((to, from, next) => {
  //全局配置修改网页标签标题
  //在标题后添加系统名称
  document.title = to.meta.title + '-' + projectNameGlobal

  //权限验证，部分路由需用户登录后才可以导航，通过判断用户是否登录实现（token是否存在）
  //在路由地址对象中，部分包含unRequiresAuth变量配置，即不需要登录权限验证即可路由导航
  //获取目标路由对象中的unRequiresAuth，如果为true，则不需要登录权限验证，如果未定义或者false，则需要权限验证
  const unRequiresAuth = to.meta.unRequiresAuth
  if (!unRequiresAuth) {//需要权限验证
    //如果请求地址以/user开头，用户路由导航
    if (to.path.startsWith('/user')) {
      //获取当前登录用户状态管理实例对象
      const userStore = useUserStore()
      //同步token数据
      userStore.doSync()
      //判断用户是否登录
      if (!userStore.isLogin) {//用户没有登录
        ElMessage.error("请先登录！")
        next('/login'); //跳转至登录页面
        return
      }
    }
  }
  next() //继续导航
})

export default router
