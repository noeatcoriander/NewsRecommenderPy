<template>
  <el-result icon="error" title="404" sub-title="页面不存在！" style="margin-top: 10%">
    <template #extra>
      <el-button type="warning" @click="router.replace('/')">返回首页</el-button>
    </template>
  </el-result>
</template>

<script setup>
import { useRouter } from "vue-router"

//获取全局路由器实例对象
const router = useRouter()
</script>

<style scoped>

</style>