/**
 * mutations业务层数据提交
 */

import storage from './../utils/storage'

/**
* `export default` 表示这个文件默认导出一个对象。  
* 在这个对象中，定义了一个名为 `saveUserToken` 的方法。这个方法是一个 Vuex mutation，它用于更改 Vuex store 中的状态。  
* `saveUserToken` 方法接受两个参数：`state` 和 `userToken`。  
	+ `state` 是 Vuex store 的当前状态对象。  
	+ `userToken` 是传入的新用户令牌。  
* `state.userToken = userToken`：这行代码将 `state` 对象中的 `userToken` 属性设置为传入的 `userToken` 值。这样，Vuex store 中的 `userToken` 状态就被更新了。  
* `storage.setItem('userToken', userToken)`：这行代码调用之前导入的 `storage` 模块的 `setItem` 方法，将 `userToken` 存储在客户端的存储中（可能是 `localStorage` 或 `sessionStorage`）。这样，即使在页面刷新或重新加载后，`userToken` 也可以被持久保存。
 */

export default {
  saveUserToken(state, userToken) {
    state.userToken = userToken
    storage.setItem('userToken', userToken)
  },
  saveUserInfo(state, userInfo) {
    state.userInfo = userInfo
    storage.setItem('userInfo', userInfo)
  },
}
