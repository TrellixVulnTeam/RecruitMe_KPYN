% rebase('master.tpl', title='Login')

<form action="login" method="POST">
  <div>
    <label>Username: </label>
    <input name="username" placeholder="username" value="{{username}}" />
  </div>
  <div>
    <label>Password: </label>
    <input name="password" placeholder="password" value="{{password}}" />
  </div>    
  <button type="submit">Login</button>
  <label class="error">{{message}}</label>
</form>