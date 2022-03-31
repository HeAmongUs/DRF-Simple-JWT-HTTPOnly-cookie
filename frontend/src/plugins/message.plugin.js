export default {
  install: (app) => {
    app.config.globalProperties.$message = function (html) {
      window.M.toast({ html })
    }
    app.config.globalProperties.$errorMessage = function (html) {
      window.M.toast({ html: `[Ошибка]: ${html}` })
    }
  },
}
