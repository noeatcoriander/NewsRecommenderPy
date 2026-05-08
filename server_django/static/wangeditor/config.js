//wangeditor富文本框配置
//html页面加载完成事件监听器
document.addEventListener('DOMContentLoaded', function () {
    //获取新闻内容字段的textarea元素（django-admin默认id为id_introduction）
    const textarea = document.getElementById('id_introduction')
    if (textarea) {
        //隐藏原生textarea文本域输入框
        textarea.style.display = 'none'

        //创建wangeditor富文本框的编辑器配置对象
        const editorConfig = {
            placeholder: '请输入新闻内容...', //编辑器提示信息
            maxLength: 30000, //最大内容长度
            xss: {ignore: true}, //关闭XSS防御配置
            allowedTags: true, //允许所有HTML标签
            allowedAttributes: true, //允许所有HTML标签属性
            pasteFilter: false, //关闭复制粘贴过滤
            autoFormat: false, //禁用自动格式化，防止内容被修改
            autoAddP: false, //禁用自动添加<p>标签
            MENU_CONF: {
                uploadImage: { //图片上传配置
                    allowPasteImage: true, //允许复制粘贴图片
                    allowDrag: true, //允许图片拖拽上传
                    server: '/api/admin/public/doEditorUpload', //图片上传后端地址
                    maxFileSize: 10 * 1024 * 1024, //图片上传最大大小，单位MB
                    allowedFileTypes: 'image/jpg,image/jpeg,image/png,image/bmp,image/webp'.split(','), //允许上传的图片类型
                    maxNumberOfFiles: 10, //最多可上传图片数量，默认100
                    fieldName: 'file', //上传字段名，即上传到后端的图片文件变量名，默认'wangeditor-uploaded-image'
                    //自定义上传参数：CSRF
                    meta: {
                        csrfmiddlewaretoken: document.querySelector("input[name='csrfmiddlewaretoken'][type='hidden']").value,
                    },
                    timeout: 10000, //请求超时时间，默认10秒
                    //图片上传成功之后的回调函数
                    onSuccess(file, res) {
                        console.log(`${file.name} 上传成功`, res)
                    },
                    //图片上传失败之后的回调函数
                    onFailed(file, res) {
                        console.log(`${file.name} 上传失败`, res)
                        const message = res.message ? res.message : '上传失败！'
                        alert(message)
                    },
                    //图片上传错误之后的回调函数，系统运行异常或请求超时
                    onError(file, err, res) {
                        console.log(`${file.name} 上传出错`, err, res)
                        alert('上传失败！')
                    }
                },
                uploadVideo: { //禁用视频上传
                    disabled: true
                }
            }
        }

        //创建wangeditor富文本框的工具栏配置对象
        const toolbarConfig = {
            excludeKeys: ['uploadVideo'] //取消视频上传按钮
        }

        //创建一个div元素
        const contentContainer = document.createElement('div')
        //div元素样式
        contentContainer.style.border = '1px solid #ccc'
        //在新闻内容文本域输入框前插入div元素
        textarea.parentNode.appendChild(contentContainer)

        //创建wangeditor富文本框工具栏容器div元素
        const toolbarContainer = document.createElement('div')
        //div元素样式
        toolbarContainer.style.borderBottom = "1px solid #ccc"
        contentContainer.appendChild(toolbarContainer)

        //创建wangeditor富文本框编辑器容器div元素
        const editorContainer = document.createElement('div')
        //div元素样式
        editorContainer.style.height = '300px'
        editorContainer.style.overflowY = 'auto'
        contentContainer.appendChild(editorContainer)

        //初始化wangeditor富文本框编辑器
        const editor = window.wangEditor.createEditor({
            selector: editorContainer, //绑定div元素
            mode: 'default', //模式：默认
            config: editorConfig //配置
        })

        //初始化wangeditor富文本框工具栏
        const toolbar = window.wangEditor.createToolbar({
            editor, //编辑器
            selector: toolbarContainer, //绑定div元素
            mode: 'default', //模式：默认
            config: toolbarConfig //配置
        })

        //初始化编辑器内容
        setTimeout(() => {
            if (textarea.value) {
                //回显修改的新闻内容
                editor.dangerouslyInsertHtml(textarea.value)
            }
        }, 1000)

        //提交表单时，将编辑器内容同步到textarea文本域输入框
        document.querySelector('form').addEventListener('submit', function () {
            //获取新闻内容数据，html格式
            let introductionHtml = editor.getHtml()
            //获取新闻内容数据，text格式
            let introductionText = editor.getText().trim()
            //判断新闻内容是否为空，或者包含图片或者包含视频
            if ((introductionText !== null && introductionText !== '')
                || introductionHtml.indexOf('<img') > 0
                || introductionHtml.indexOf('<video') > 0) {
                textarea.value = editor.getHtml()
            }
        })
    }
});