/**
 * pinia前端用户状态管理配置文件
 * 保存登录用户信息，所有组件都可使用
 * 原理：当用户登录后将用户信息和token同时保存在pinia和localStorage中
 * pinia是vue3推荐的状态管理库，主要用于保存共享数据，所有组件都可使用，当修改登录用户信息时，使用共享数据的组件可响应式变化
 * pinia将共享数据保存在当前网页内存中，刷新网页或关闭浏览器数据消失
 * localStorage是javascript内置对象，主要用于保存共享数据，所有组件都可使用，不可响应式变化，
 * 只保存字符串类型数据，数据保存在浏览器内存中，刷新网页或关闭浏览器数据仍然存在，
 * 当手动清空浏览器缓存时，数据消失，
 * 因此，需要将登录用户信息和token同时保存在pinia和localStorage中，pinia的初始值从localStorage中获取
 */
import { defineStore } from "pinia"
import { ElMessage, ElMessageBox } from "element-plus"

//创建并暴露用户状态管理实例对象
export const useUserStore = defineStore('user', {
  //数据，从localStorage中获取保存的登录用户信息和token作为初始值
  state: () => {
    //获取登录用户信息，localStorage只保存字符串类型数据
    const currentUserInfo = localStorage.getItem('currentUserInfo')
    return {
      user: currentUserInfo ? JSON.parse(currentUserInfo) : {}, //将字符串用户信息转json格式，并获取
      token: localStorage.getItem('currentUserToken') || null //获取token
    }
  },
  //计算属性
  getters: {
    //判断用户是否已登录，通过判断token是否存在获取
    isLogin: (state) => !!state.token
  },
  //方法
  actions: {
    //保存登录用户信息和token
    doSave(user, token) {
      //保存登录用户信息到pinia
      this.user = { ...user } //通过复制变量的形式保存
      //保存登录用户信息到localStorage
      localStorage.setItem('currentUserInfo', JSON.stringify(user))
      //保存token到pinia
      this.token = token
      //保存token到localStorage
      localStorage.setItem('currentUserToken', token)
    },
    //更新登录用户信息
    doUpdate(newUser) {
      //保存登录用户信息到pinia
      this.user = { ...newUser }
      //保存登录用户信息到localStorage
      localStorage.setItem('currentUserInfo', JSON.stringify(newUser))
    },
    //登录提示
    doIsLogin() {
      if (!this.isLogin) {
        ElMessage.error('请先登录！')
      }
      return this.isLogin
    },
    //删除登录信息
    doRemove() {
      if (this.isLogin) {
        //删除登录用户信息
        this.user = {}
        localStorage.removeItem('currentUserInfo')
        //删除token
        this.token = null
        localStorage.removeItem('currentUserToken')
      }
    },
    //退出登录
    doLogout(router) {
      ElMessageBox.confirm('确认退出登录？', '退出登录', { type: 'warning' }).then(() => {
        this.doRemove()
        router.replace('/') //跳转到首页
      }).catch(() => {
        //取消退出登录
      })
    },
    //同步pinia和localStorage中的登录用户信息和token
    //pinia数据保存在浏览器的网页内存中，localStorage保存在浏览器内存中
    //当浏览器关闭或者浏览器网页关闭，pinin数据被删除，再次打开网页时，pinia从localStorage中获取数据
    //当手动清空浏览器缓存时，localStorage数据被删除
    //因此，当手动清空浏览器缓存时，此次网页中的pinia数据仍然存在，localStorage中数据被删除，导致数据不同步
    //在全局前置路由守卫中使用
    doSync() {
      //获取token
      const localToken = localStorage.getItem('currentUserToken')
      //获取登录用户信息
      const localUser = localStorage.getItem('currentUserInfo')
      //同步
      if (this.token !== localToken) {
        this.token = localToken || null
        this.user = localUser || {}
      }
    }
  }
})