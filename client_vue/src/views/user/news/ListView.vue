<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">新闻分类</div>
    </div>
    <!--新闻类型-->
    <div class="search-newstype">
      <el-button link size="large" @click="doSearchNewstype()" :class="{ 'active-button': data.newstypeid === '' }">
        全部分类
      </el-button>
      <template v-for="newstype in data.newstypeList" :key="newstype.id">
        <el-divider direction="vertical"/>
        <el-button link size="large" @click="doSearchNewstype(newstype.id)"
                   :class="{ 'active-button': data.newstypeid === newstype.id }">
          {{ newstype.newstypename }}
        </el-button>
      </template>
    </div>
    <!--新闻列表-->
    <div class="grid-container" v-if="data.newsList && data.newsList.length > 0">
      <el-card v-for="news in data.newsList" :key="news.id" shadow="never"
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
    <!--分页-->
    <div class="pagination">
      <el-pagination
          style="overflow: auto"
          v-model:current-page="data.pageNum"
          v-model:page-size="data.pageSize"
          :total="data.total"
          :page-sizes="pageSizesGlobal"
          background
          layout="total, sizes, prev, pager, next, jumper"/>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from "@/tool/request"
import { baseUploadUrlGlobal, pageSizeGlobal, pageSizesGlobal } from "@/tool/public"

//获取全局路由器实例对象
const router = useRouter()
//获取当前路由实例对象
const route = useRoute()

//创建页面的响应式数据对象
const data = reactive({
  newstypeid: Number(route.query.newstypeid) || '', //新闻类型id
  newstypeList: [], //新闻类型列表
  newsList: [], //新闻列表
  pageNum: Number(route.query.pageNum) || 1, //分页，当前页数
  //分页，每页条数，先判断路由参数中的每页条数pageSize是否在设置的每页条数数组中pageSizesGlobal，如果不在则选择默认每页条数pageSizeGlobal，
  //如果在则选择路由参数中的route.query.pageSize
  pageSize: pageSizesGlobal.includes(Number(route.query.pageSize)) ? Number(route.query.pageSize) : pageSizeGlobal,
  total: 0 //分页，数据总量
})

//创建获取路由地址参数的函数
const getRouteQuery = () => (
    {
      keywords: route.query.keywords || '', //搜索关键字
      newstypeid: route.query.newstypeid || '', //新闻类型id
      pageNum: Number(route.query.pageNum) || 1, //分页，当前页数
      //分页，每页条数
      pageSize: pageSizesGlobal.includes(Number(route.query.pageSize)) ? Number(route.query.pageSize) : pageSizeGlobal
    }
)

//创建查询新闻列表数据函数
const loadData = () => {
  //获取路由参数，并异步请求后端数据
  request.get('/user/news/list', {
    params: getRouteQuery()
  }).then(res => {
    //解析后端返回的数据
    data.newstypeList = res.newstypeList //新闻类型列表
    data.newsList = res.pageBean.list //新闻列表
    data.newstypeid = res.newstypeid || '' //新闻类型id
    data.pageNum = res.pageBean.pageNum //分页，当前页数
    data.pageSize = res.pageBean.pageSize //分页，每页条数
    data.total = res.pageBean.total //分页，数据总量
  })
}

//创建搜索新闻类型函数
const doSearchNewstype = (newstypeid = '') => {
  data.newstypeid = newstypeid //修改响应式数据：新闻类型id，实现新闻类型按钮变色
  //路由导航，即重新执行当前页面的路由导航，添加参数：pageNum、newstypeid
  router.push({ query: { ...route.query, pageNum: 1, newstypeid: newstypeid } })
}

//监听事件，监听当前页数变化
watch(
    () => data.pageNum,
    (newPageNum) => {
      //当新页数与路由参数中的页数不同，同时每页条数没有变化时，进行路由导航
      if (newPageNum !== getRouteQuery().pageNum && data.pageSize === getRouteQuery().pageSize) {
        //路由导航，即重新执行当前页面的路由导航，添加参数：pageNum
        router.push({ query: { ...route.query, pageNum: newPageNum } })
      }
    }
)

//vue watch监听事件，监听页面条数变化
watch(() => data.pageSize,
    (newPageSize) => {
      //当新页面条数与路由参数中的页面条数不同，进行路由导航
      if (newPageSize !== getRouteQuery().pageSize) {
        data.pageNum = 1 //修改当前页数为1，避免element plus自动修改
        //路由导航，即重新执行当前页面的路由导航，添加参数：pageNum、pageSize
        router.push({ query: { ...route.query, pageNum: 1, pageSize: newPageSize } })
      }
    }
)

//vue watch监听事件，监听路由参数变化
watch(
    () => route.query,
    (newQuery, oldQuery) => {
      loadData() //加载数据
    },
    { deep: true }
)

//加载数据
loadData()
</script>

<style scoped>

</style>