<!--前台用户布局页面-->
<template>
  <div class="layout-container">
    <el-container>
      <!--页面头部-->
      <el-header>
        <Header/>
      </el-header>
      <!--页面banner-->
      <div>
        <Banner/>
      </div>
      <!--页面内容-->
      <el-main>
        <!--路由视图容器，根据访问的路由地址自动渲染显示的组件-->
        <router-view/>
      </el-main>
      <!--页面尾部-->
      <el-footer>
        <Footer/>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
/*导入自定义样式文件*/
import '@/style/css_user.css'
import Header from "@/components/user/Header.vue"
import Footer from "@/components/user/Footer.vue"
import Banner from "@/components/user/Banner.vue"
</script>

<style scoped>
/*页面头部样式*/
.layout-container .el-container .el-header {
  background-color: unset;
  height: 65px;
  padding: 0 40px;
}

/*页面内容样式*/
.layout-container > .el-container > .el-main {
  padding: 20px 40px;
  min-height: 50vh;
}

/*页面尾部样式*/
.layout-container .el-container .el-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: #AF967F;
  color: white;
  font-size: 90%;
}
</style>