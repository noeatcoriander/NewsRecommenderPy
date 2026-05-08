<!--前台用户页面头部组件-->
<template>
  <div class="header-container">
    <el-row align="middle" class="header-row">
      <el-col :span="7" class="header-left">
        <el-link href="/" underline="never" class="logo-link" :title="projectNameGlobal">
          {{ projectNameGlobal }}
        </el-link>
      </el-col>
      <el-col :span="9" class="header-center">
        <el-input v-model.trim="keywords" @keyup.enter="doSearch" size="large"
                  placeholder="搜索新闻标题、新闻来源"
                  class="search-input" maxlength="255"/>
        <el-button link size="large" title="搜索" @click="doSearch"
                   style="padding: 0 20px;color: #582F0E;font-size: 15px;">搜索
        </el-button>
      </el-col>
      <el-col :span="8" class="header-right">
        <el-button link size="large" class="header-button" @click="router.push('/')">首页</el-button>
        <el-button link size="large" class="header-button" @click="router.push('/user/news/list')">新闻分类</el-button>
        <template v-if="userStore.isLogin">
          <el-dropdown>
            <span class="el-dropdown-link header-button">
              <el-image :src="baseUploadUrlGlobal+userStore.user?.avatar" fit="fill"
                        style="width: 40px;height: 40px;border-radius: 4px;"/>
              &nbsp;
              {{
                userStore.user?.loginname.length > 6 ? userStore.user?.loginname.slice(0, 6) + '...' : userStore.user?.loginname
              }}
              <el-icon class="el-icon--right">
                <CaretBottom/>
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/user/user/detail')">
                  个人信息
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/user/userlabel/update')">
                  兴趣标签
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/user/userscore/list')">
                  我的评分
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/user/userreview/list')">
                  我的评论
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/user/userbrowse/list')">
                  浏览历史
                </el-dropdown-item>
                <el-dropdown-item @click="userStore.doLogout(router)">
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button link size="large" class="header-button" @click="router.push('/register')">用户注册</el-button>
          <el-button link size="large" class="header-button" @click="router.push('/login')">用户登录</el-button>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { baseUploadUrlGlobal, projectNameGlobal } from "@/tool/public"
import { useRoute, useRouter } from 'vue-router'
import { ref, watch } from "vue"
import { useUserStore } from "@/store/userStore"

//获取全局路由器实例对象
const router = useRouter()
//获取当前路由实例对象
const route = useRoute()
//获取当前登录用户状态管理实例对象
const userStore = useUserStore()

//创建搜索关键字响应式数据对象，初始值：路由地址的搜索关键字参数
const keywords = ref(route.query.keywords || '')

//搜索函数
const doSearch = () => {
  //路由导航，跳转到新闻分类页面，路由参数：搜索关键字
  router.push({ path: '/user/news/list', query: { keywords: keywords.value } })
}

//vue watch监听事件，监听路由参数
//当点击新闻分类时，清空搜索框内容
watch(
    () => route.query,
    () => {
      //只在新闻分类页面从路由地址获取搜索关键字参数
      if (route.path.startsWith('/user/news/list')) {
        keywords.value = typeof route.query.keywords === 'string' ? route.query.keywords : ''
      } else {
        keywords.value = ''
      }
    }
)
</script>

<style scoped>
/*页面头部样式*/
.header-container {
  height: 100%;
  border: 0;
  margin: 0 20px;
}

.header-row {
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-link {
  font-size: 23px;
  color: #582F0E;
}

.header-center {
  display: flex;
  justify-content: center;
}

.search-input {
  width: 80%;
}

.header-right {
  display: flex;
  flex-wrap: wrap;
  justify-content: right;
  align-items: center;
}

.header-button {
  font-size: 15px;
  color: #582F0E;
  margin-left: 10px;
  margin-right: 10px;
}

/*下拉菜单样式*/
.el-dropdown {
  line-height: initial;
  color: initial;
  font-size: initial;
}

.el-dropdown i {
  vertical-align: middle;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  outline: unset !important;
}

/*下拉菜单是element plus使用了vue的插槽用法：<template #dropdown>
即下拉菜单中显示的内容是下拉菜单的子组件
故需要使用:deep穿透样式*/
:deep(.el-dropdown-menu__item) {
  padding: 6px 40px;
}
</style>