<!--前台用户页面菜单组件-->
<template>
  <div>
    <el-menu :router="true" :default-active="activeMenu">
      <el-menu-item index="/user/user/detail">
        <span>个人信息</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="/user/userlabel/update">
        <span>兴趣标签</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="/user/userscore/list">
        <span>我的评分</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="/user/userfavor/list">
        <span>我的收藏</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="/user/userlike/list">
        <span>我的点赞</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="/user/userreview/list">
        <span>我的评论</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="/user/userbrowse/list">
        <span>浏览历史</span>
        <el-icon>
          <ArrowRight/>
        </el-icon>
      </el-menu-item>
      <el-menu-item index="" @click="userStore.doLogout(router)">
        <span>退出登录</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, watch } from 'vue'
import { useUserStore } from "@/store/userStore"

//获取全局路由器实例对象
const router = useRouter()
//获取当前路由实例对象
const route = useRoute()
//获取当前登录用户状态管理实例对象
const userStore = useUserStore()

//创建选中菜单的响应式对象
//element plus通过对比activeMenu值与当前路由地址是否相同，以选中菜单
const activeMenu = ref('')

//vue watch监听事件
//监听当前路由实例对象的parentMenu值，该值在路由配置文件中配置
watch(() => route.meta.parentMenu, (parentPath) => {
  //设置选中菜单的路由地址，当前路由实例对象的parentMenu值或者当前路由地址
  activeMenu.value = parentPath || route.path
}, { immediate: true, deep: true })
</script>

<style scoped>
/*菜单激活选中样式*/
.el-menu-item:hover, .el-menu-item.is-active {
  background-color: unset;
  font-weight: 600;
}

.el-menu-item {
  justify-content: space-between;
  border-bottom: 1px solid var(--el-menu-border-color);
  font-size: 15px;
}

.el-menu-item .el-icon {
  font-size: 100%;
}

.el-menu {
  border: 0;
}
</style>