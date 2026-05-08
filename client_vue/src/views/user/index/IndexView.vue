<!--前台用户首页-->
<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">个性化推荐</div>
    </div>
    <div class="grid-container" v-if="data.recommendList && data.recommendList.length > 0">
      <el-card v-for="news in data.recommendList" :key="news.id" shadow="never"
               class="grid-card" body-style="padding: 0;" style="border: 0;border-radius: 0;">
        <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title">
          <el-image :src="baseUploadUrlGlobal + news.photo" class="card-image" fit="fill">
            <template #error>
              <div class="el-image card-image">
                <div class="el-image__error">
                  <div class="text-break" style="padding: 8px 8px;color: #62656f;">
                    {{ news.title.length > 50 ? news.title.slice(0, 50) + '...' : news.title }}
                  </div>
                </div>
              </div>
            </template>
          </el-image>
        </router-link>
        <div class="card-content">
          <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title"
                       class="el-link card-name text-break">
            {{ news.title.length > 18 ? news.title.slice(0, 18) + '...' : news.title }}
          </router-link>
          <p class="card-text text-break" style="margin-top: 10px;">
            <span>{{ news.newssource }}</span>
          </p>
          <el-divider style="margin: 15px 0 5px 0;"/>
        </div>
      </el-card>
    </div>
    <div v-else class="data-empty">暂无数据！</div>
  </div>
  <div class="main-container" v-if="data.recommendBasedLabelList && data.recommendBasedLabelList.length > 0">
    <div class="main-title" style="justify-content: unset;">
      <div class="title-name">兴趣标签推荐</div>
      <div style="font-size: small;padding-left: 40px;">
        <a href="#" @click.prevent="loadRecommendBasedLabelData" class="el-link">换一换</a>
      </div>
    </div>
    <div class="grid-container" v-if="data.recommendBasedLabelList && data.recommendBasedLabelList.length > 0">
      <el-card v-for="news in data.recommendBasedLabelList" :key="news.id" shadow="never"
               class="grid-card" body-style="padding: 0;" style="border: 0;border-radius: 0;">
        <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title">
          <el-image :src="baseUploadUrlGlobal + news.photo" class="card-image" fit="fill">
            <template #error>
              <div class="el-image card-image">
                <div class="el-image__error">
                  <div class="text-break" style="padding: 8px 8px;color: #62656f;">
                    {{ news.title.length > 50 ? news.title.slice(0, 50) + '...' : news.title }}
                  </div>
                </div>
              </div>
            </template>
          </el-image>
        </router-link>
        <div class="card-content">
          <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title"
                       class="el-link card-name text-break">
            {{ news.title.length > 18 ? news.title.slice(0, 18) + '...' : news.title }}
          </router-link>
          <p class="card-text text-break" style="margin-top: 10px;">
            <span>{{ news.newssource }}</span>
          </p>
          <el-divider style="margin: 15px 0 5px 0;"/>
        </div>
      </el-card>
    </div>
    <div v-else class="data-empty">暂无数据！</div>
  </div>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">点赞排行</div>
    </div>
    <div class="grid-container" v-if="data.newsTopByLike && data.newsTopByLike.length > 0">
      <el-card v-for="news in data.newsTopByLike" :key="news.id" shadow="never"
               class="grid-card" body-style="padding: 0;" style="border: 0;border-radius: 0;">
        <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title">
          <el-image :src="baseUploadUrlGlobal + news.photo" class="card-image" fit="fill">
            <template #error>
              <div class="el-image card-image">
                <div class="el-image__error">
                  <div class="text-break" style="padding: 8px 8px;color: #62656f;">
                    {{ news.title.length > 50 ? news.title.slice(0, 50) + '...' : news.title }}
                  </div>
                </div>
              </div>
            </template>
          </el-image>
        </router-link>
        <div class="card-content">
          <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title"
                       class="el-link card-name text-break">
            {{ news.title.length > 18 ? news.title.slice(0, 18) + '...' : news.title }}
          </router-link>
          <p class="card-text text-break" style="margin-top: 10px;">
            <span>{{ news.newssource }}</span>
          </p>
          <el-divider style="margin: 15px 0 5px 0;"/>
        </div>
      </el-card>
    </div>
    <div v-else class="data-empty">暂无数据！</div>
  </div>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">收藏排行</div>
    </div>
    <div class="grid-container" v-if="data.newsTopByFavor && data.newsTopByFavor.length > 0">
      <el-card v-for="news in data.newsTopByFavor" :key="news.id" shadow="never"
               class="grid-card" body-style="padding: 0;" style="border: 0;border-radius: 0;">
        <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title">
          <el-image :src="baseUploadUrlGlobal + news.photo" class="card-image" fit="fill">
            <template #error>
              <div class="el-image card-image">
                <div class="el-image__error">
                  <div class="text-break" style="padding: 8px 8px;color: #62656f;">
                    {{ news.title.length > 50 ? news.title.slice(0, 50) + '...' : news.title }}
                  </div>
                </div>
              </div>
            </template>
          </el-image>
        </router-link>
        <div class="card-content">
          <router-link :to="'/user/news/detail?newsid='+news.id" :title="news.title"
                       class="el-link card-name text-break">
            {{ news.title.length > 18 ? news.title.slice(0, 18) + '...' : news.title }}
          </router-link>
          <p class="card-text text-break" style="margin-top: 10px;">
            <span>{{ news.newssource }}</span>
          </p>
          <el-divider style="margin: 15px 0 5px 0;"/>
        </div>
      </el-card>
    </div>
    <div v-else class="data-empty">暂无数据！</div>
  </div>

</template>

<script setup>
import { reactive } from 'vue'
import request from "@/tool/request"
import { baseUploadUrlGlobal } from "@/tool/public"
import { useRouter } from "vue-router"
import { useUserStore } from "@/store/userStore"

//获取全局路由器实例对象
const router = useRouter()
//获取当前登录用户的状态管理实例对象
const userStore = useUserStore()

//创建页面的响应式数据对象
const data = reactive({
  recommendList: [], //个性化推荐新闻列表
  recommendBasedLabelList: [], //兴趣标签推荐新闻列表
  newsTopByLike: [], //点赞排行新闻列表
  newsTopByFavor: [] //收藏排行新闻列表
})

//创建查询个性化推荐新闻数据函数
const loadRecommendData = () => {
  //请求数据
  request.get('/user/index/recommend').then(res => {
    data.recommendList = res.recommendList //个性化新闻推荐列表
    loadRecommendBasedLabelData() //加载兴趣标签推荐新闻列表
  })
}

//创建查询兴趣标签推荐新闻数据函数
const loadRecommendBasedLabelData = () => {
  if (userStore.isLogin) {//判断用户是否已登录
    //请求数据
    request.get('/user/index/recommendBasedLabel').then(res => {
      data.recommendBasedLabelList = res.recommendBasedLabelList //兴趣标签推荐新闻列表
    })
  }
}

//创建查询点赞排行、收藏排行数据函数
const loadTopData = () => {
  //请求数据
  request.get('/user/index/top').then(res => {
    data.newsTopByLike = res.newsTopByLike //点赞排行新闻列表
    data.newsTopByFavor = res.newsTopByFavor //收藏排行新闻列表
  })
}

//加载数据
loadRecommendData()
loadTopData()
</script>

<style scoped>

</style>