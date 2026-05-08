<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">查看评论</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div>
              <el-form label-width="25%" style="max-width: 90%" label-suffix="：">
                <el-row :gutter="10">
                  <el-col v-if="data.userreview.news?.photo" :span="5">
                    <el-form-item label-width="10%" style="margin-top: 10px;">
                      <el-image :src="baseUploadUrlGlobal+data.userreview.news?.photo" fit="fill"
                                style="width: 100%;"/>
                    </el-form-item>
                  </el-col>
                  <el-col v-else :span="5"></el-col>
                  <el-col :span="19">
                    <el-form-item label="新闻标题">
                      <router-link class="el-link text-break" :to="'/user/news/detail?newsid='+data.userreview.newsid">
                        {{ data.userreview.news?.title }}
                      </router-link>
                    </el-form-item>
                    <el-form-item label="评论内容">
                      <div class="text-break" style="line-height: normal">{{ data.userreview.introduction }}</div>
                    </el-form-item>
                    <el-form-item label="评论时间">{{ data.userreview.savedate }}</el-form-item>
                  </el-col>
                </el-row>
                <div style="display: flex;justify-content: center;margin: 30px 0;">
                  <el-button type="warning"
                             @click="router.push('/user/userreview/update?userreviewid='+data.userreview.id)">
                    修改评论
                  </el-button>
                </div>
              </el-form>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import Menu from "@/components/user/Menu.vue"
import { reactive } from 'vue'
import request from "@/tool/request"
import { useRoute, useRouter } from "vue-router"
import { baseUploadUrlGlobal } from "@/tool/public"

//获取全局路由器实例对象
const router = useRouter()
//获取当前路由实例对象
const route = useRoute()

//从路由地址的参数中获取评论id
const userreviewid = route.query.userreviewid || ''

//创建页面的响应式数据对象
const data = reactive({
  userreview: {} //表单数据对象
})

//加载数据
const loadData = () => {
  if (userreviewid) {
    //请求数据
    request.get('/user/userreview/detail?userreviewid=' + userreviewid).then(res => {
      data.userreview = res.userreview ? res.userreview : {}
    })
  }
}

//加载数据
loadData()
</script>

<style scoped>

</style>