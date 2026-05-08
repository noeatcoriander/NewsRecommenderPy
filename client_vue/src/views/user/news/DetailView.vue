<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">新闻详情</div>
    </div>
    <div v-if="data.news" class="main-content">
      <el-row :gutter="50">
        <el-col v-if="data.news.photo" :span="6">
          <el-image :src="baseUploadUrlGlobal+data.news.photo" fit="fill"/>
        </el-col>
        <el-col v-else :span="4"></el-col>
        <el-col :span="18">
          <h2 class="text-break" style="margin-top: 0;margin-bottom: 30px;text-align: center;font-weight: normal;
            color: #582F0E;">{{ data.news.title }}</h2>
          <ul>
            <li>新闻类型：{{ data.newstype.newstypename }}</li>
            <li>上传时间：{{ data.news.savedate }}</li>
          </ul>
          <ul>
            <li style="width: 100%;">新闻来源：{{ data.news.newssource }}</li>
          </ul>
          <div>
            <div style="display: flex;justify-content: space-between;margin-bottom: 10px">
              <span>平均评分：{{ data.scoreTool?.scoreAvg }}</span>
              <span>评分数量：{{ data.scoreTool?.scoreCount }}</span>
              <span>点赞数量：{{ data.userlikeCount }}</span>
              <span>收藏数量：{{ data.userfavorCount }}</span>
              <span>点击数量：{{ data.news.clicks }}</span>
            </div>
            <div style="margin-top: 30px;display: flex;align-items: center;">
              <div>新闻评分：&nbsp;&nbsp;&nbsp;&nbsp;</div>
              <div style="width: 50%">
                <table class="el-table" style="font-size: 14px">
                  <tr v-for="(currentScoreTool,index) in data.scoreTool?.currentScoreToolList" :key="index">
                    <td style="width: 50px">{{ currentScoreTool.currentScore }} 星</td>
                    <td>
                      <el-progress :stroke-width="18" :percentage="currentScoreTool.percent" color="#f2b952"/>
                    </td>
                  </tr>
                </table>
              </div>
            </div>
          </div>
          <div class="detail-button" style="margin-top: 30px;">
            <el-button v-if="data.userfavor" link size="large" class="active" @click="doUserfavor" title="取消收藏">
              取消收藏
            </el-button>
            <el-button v-else link size="large" @click="doUserfavor" title="添加收藏">
              添加收藏
            </el-button>
            <el-button v-if="data.userlike" link size="large" class="active" title="取消点赞" @click="doUserlike"
                       style="margin-left: 80px">取消点赞
            </el-button>
            <el-button v-else link size="large" title="添加点赞" @click="doUserlike" style="margin-left: 80px">添加点赞
            </el-button>
            <div class="score" style="display: inline-flex;margin-left: 80px">
              添加评分：&nbsp;&nbsp;
              <el-rate size="large" @change="doUsescore" v-model="data.userscore"/>
            </div>
          </div>
        </el-col>
      </el-row>
      <div class="content-item">
        <div class="title">新闻内容：</div>
        <div v-html="handleNewsContent(data.news.introduction)" class="text-break news-content"
             style="border-radius: 4px;background-color: #f5f7fa;font-size: 95%;padding: 20px 20px"/>
      </div>
      <div class="content-item">
        <div class="title" style="display: flex;">
          <div style="width: 100px;">猜你喜欢：</div>
          <div style="font-size: small;">
            <a href="#" @click.prevent="loadRecommendData" class="el-link">换一换</a>
          </div>
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
      <div class="content-item" style="margin-top: -20px;">
        <div class="title">新闻评论：</div>
        <div>
          <el-row :gutter="30">
            <el-col :span="18">
              <el-form ref="commentFormRef" :rules="data.commentFormRules" :model="data.commentFormModel"
                       label-width="auto" label-suffix="：">
                <el-form-item label="评论内容" prop="introduction">
                  <el-input type="textarea" v-model.trim="data.commentFormModel.introduction" maxlength="2000"
                            :rows="5" placeholder="请输入评论内容"/>
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="6" style="align-content: center;">
              <el-button type="warning" @click="doUserreview">提交评论</el-button>
            </el-col>
          </el-row>
          <el-row :gutter="30">
            <el-col :span="24">
              <el-row v-if="data.userreviewList && data.userreviewList.length > 0"
                      v-for="userreview in data.userreviewList" :key="userreview.id" :gutter="20"
                      style="margin-bottom: 20px;">
                <el-col :span="2">
                  <el-image :src="baseUploadUrlGlobal+userreview.user.avatar" fit="fill"/>
                </el-col>
                <el-col :span="22">
                  <div class="text-break"
                       style="margin-bottom: 10px;display: flex;justify-content: space-between;align-items: center;
                       border-radius: 4px;background-color: #f5f7fa;padding: 15px 15px">
                    <span style="font-size: 95%">评论用户：{{ userreview.user.loginname }}</span>
                    <span style="font-size: 95%">评论时间：{{ userreview.savedate }}</span>
                  </div>
                  <div class="text-break"
                       style="font-size: 90%;padding: 15px 15px;color: #333333;">
                    {{ userreview.introduction }}
                  </div>
                </el-col>
              </el-row>
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
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
    <div v-else class="main-content">
      <div class="data-empty">暂无数据！</div>
    </div>
  </div>
</template>

<script setup>
import { baseUploadUrlGlobal, pageSizeGlobal, pageSizesGlobal } from "@/tool/public"
import { reactive, ref, watch } from "vue"
import request from "@/tool/request"
import { useRoute } from 'vue-router'
import { useUserStore } from "@/store/userStore"
import { handleNewsContent } from "@/tool/tool"

//获取当前路由实例对象
const route = useRoute()
//获取当前登录用户的状态管理实例对象
const userStore = useUserStore()

//获取当前新闻id，从路由地址参数中获取
let newsid = route.query.newsid || ''

//创建评论表单组件的引用实例对象，可调用表单的属性和方法
const commentFormRef = ref()

//创建页面的响应式数据对象
const data = reactive({
  news: null, //当前新闻对象
  newstype: {}, //当前新闻的新闻类型对象
  userlike: false, //当前登录用户对当前新闻是否已点赞
  userfavor: false, //当前登录用户对当前新闻是否已收藏
  userscore: 0, //当前登录用户对当前新闻的评分值
  userlikeCount: 0, //当前新闻的点赞数量
  userfavorCount: 0, //当前新闻的收藏数量
  scoreTool: {}, //当前新闻的评分分析对象
  recommendList: [], //推荐新闻列表
  commentFormModel: {}, //评论表单数据对象
  commentFormRules: { //评论表单数据校验对则对象
    introduction: [
      { required: true, message: '请输入评论内容', trigger: 'blur' }
    ]
  },
  userreviewList: [], //评论列表
  pageNum: 1, //分页，当前页数
  pageSize: pageSizeGlobal, //分页，每页条数
  total: 0 //分页，数据总量
})

//获取当前新闻详情函数
const loadData = () => {
  if (newsid) {
    //请求数据
    request.get('/user/news/detail?newsid=' + newsid).then(res => {
      if (res.news) {
        data.news = res.news //新闻
        data.newstype = res.newstype //当前新闻的新闻类型
      } else {
        data.news = null
      }
    })
  }
}

//获取当前新闻的数据分析函数
const loadAnalysisNewsData = () => {
  if (newsid) {
    //请求数据
    request.get('/user/news/doAnalysisNewsData?newsid=' + newsid).then(res => {
      data.userlikeCount = res.userlikeCount //当前新闻的点赞量
      data.userfavorCount = res.userfavorCount //当前新闻的收藏量
      data.scoreTool = res.scoreTool //当前新闻的评分分析
    })
  }
}

//获取当前登录用户对当前新闻的数据分析函数
const loadAnalysisUserData = () => {
  if (newsid) {
    if (userStore.isLogin) {//判断用户是否已登录
      //请求数据
      request.get('/user/news/doAnalysisUserData?newsid=' + newsid).then(res => {
        data.userlike = res.userlike //点赞
        data.userfavor = res.userfavor //收藏
        data.userscore = res.userscore ? res.userscore.score : 0 //评分
      })
    }
  }
}

//新闻点赞函数
const doUserlike = () => {
  if (newsid) {
    if (userStore.doIsLogin()) {//判断用户是否已登录
      //提交数据
      request.post('/user/userlike/doUpdate', { newsid: newsid }).then(res => {
        if (res.success > 0) {//操作成功
          data.userlike = res.userlike //点赞
          loadAnalysisNewsData() //更新当前新闻的数据分析
        }
      })
    }
  }
}

//新闻收藏函数
const doUserfavor = () => {
  if (userStore.doIsLogin()) {//判断用户是否已登录
    request.post('/user/userfavor/doUpdate', { newsid: newsid }).then(res => {
      if (res.success > 0) {//操作成功
        data.userfavor = res.userfavor //收藏
        loadAnalysisNewsData() //更新当前新闻的数据分析
      }
    })
  }
}

//新闻评分函数
const doUsescore = (score) => {
  if (userStore.doIsLogin()) {//判断用户是否已登录
    request.post('/user/userscore/doUpdate', { newsid: newsid, score: score }).then(res => {
      if (res.success > 0) { //操作成功
        loadAnalysisNewsData() //更新当前新闻的数据分析
      }
    })
  }
}

//新闻评论函数
const doUserreview = () => {
  //校验评论表单数据
  commentFormRef.value.validate((valid) => {
    if (valid) {
      if (userStore.doIsLogin()) {//判断用户是否已登录
        //提交数据
        request.post('/user/userreview/doUpdate', { ...data.commentFormModel, newsid: newsid }).then(res => {
          if (res.success > 0) { //操作成功
            data.commentFormModel = {} //清空评论表单数据
            //判断当前评论列表的页面是否是第一页，
            //如果不是第一页，则修改页面，并触发页码监听器加载新评论列表数据，如果是第一页，则重新加载新评论列表数据
            if (data.pageNum === 1) {
              loadUserreviewData() //重新加载新评论列表数据
            } else {
              data.pageNum = 1 //修改页码
            }
          }
        })
      }
    }
  })
}

//获取推荐新闻函数
const loadRecommendData = () => {
  if (newsid) {
    //请求数据
    request.get('/user/news/recommend', { params: { newsid: newsid } }).then(res => {
      data.recommendList = res.recommendList
    })
  }
}

//获取当前新闻的评论列表数据函数
const loadUserreviewData = () => {
  if (newsid) {
    //请求数据
    request.get('/user/userreview/listByNewsid', {
      params: { pageNum: data.pageNum, pageSize: data.pageSize, newsid: newsid }
    }).then(res => {
      data.userreviewList = res.pageBean.list //评论列表
      data.total = res.pageBean.total //分页，数据总量
    })
  }
}

//vue watch监听事件，监听分页页码和每页显示数量的改变，改变后重新加载数据
watch(
    () => [data.pageNum, data.pageSize],
    () => {
      loadUserreviewData() //加载评论列表数据
    }
)

//加载页面所有数据
const loadAllData = () => {
  loadData() //加载当前新闻数据
  loadAnalysisNewsData() //加载当前新闻的评分分析数据
  loadUserreviewData() //加载当前新闻的评论数据
  loadAnalysisUserData() //加载当前登录用户对当前新闻的数据
  loadRecommendData() //加载推荐新闻数据
}

//vue watch监听事件，监听路由地址中的新闻id参数，并加载页面所有数据
watch(
    () => route.query.newsid, //监听新闻id
    async (newNewsId) => {
      if (newNewsId) {
        newsid = newNewsId
        //加载页面所有数据
        loadAllData()
        //页面滚动到页面顶部
        window.scrollTo({ top: 0 })
      }
    },
    { immediate: true }
)
</script>

<style scoped>
/*评分样式*/
.score .el-rate, .score .el-rate--large {
  height: unset;
}

/*新闻数据样式*/
.main-content .el-row .el-col ul {
  display: flex;
  list-style-type: none;
  margin: 20px 0;
  padding-left: 0;
  /*font-size: 95%;*/
}

.main-content .el-row .el-col ul li {
  width: 50%;
  margin-right: 20px;
  word-break: break-all;
}

.main-content .content-item {
  margin: 30px 0
}

.main-content .content-item .title {
  padding-left: 20px;
  font-weight: 500;
  color: #582F0E;
  margin: 20px 0;
}

/*评分进度条样式*/
.el-table .el-progress--line {
  margin-bottom: 5px;
}

:deep(.el-table .el-progress--line .el-progress__text) {
  font-size: 14px !important;
}

/*按钮样式*/
.detail-button .el-button {
  font-size: 100%;
  color: #582F0E;
  text-decoration: underline;
}

.detail-button .el-button:hover {
  font-weight: 600;
}

.detail-button .el-button.active {
  font-weight: 600;
}
</style>