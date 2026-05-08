<!--前台用户页面尾部组件-->
<template>
  <div class="footer-container" style="vertical-align: middle">
    <div style="display: inline-block">新手指南</div>
    <div style="display: inline-block">新闻社区</div>
    <div style="display: inline-block">用户反馈</div>
    <div style="display: inline-block">活动专区</div>
    <div style="display: inline-block">在线客服</div>
    <div style="display: inline-block">加入我们</div>
    <div style="display: inline-block">友情链接</div>
    <div style="display: inline-block">合作伙伴</div>
    <div style="display: inline-block">
      <el-link :href="baseUrl + '/admin'" style="color: white;font-size: var(--el-text-font-size);vertical-align: unset"
               target="_blank">
        后台管理
      </el-link>
    </div>
  </div>
</template>

<script setup>
import { baseUrl } from '@/tool/public'

</script>

<style scoped>
.footer-container div {
  margin: 0 20px;
}
</style>