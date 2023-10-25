import * as React from 'react';
import {useState} from 'react';
import {login, logout} from '../functions/api';
import {isLoggedIn} from '../functions/auth';

const Login: React.FC = () => {
  const [password, setPassword] = useState<string>('SlCollect202009');
  const [email, setEmail] = useState<string>('collect@seminar-live.com');
  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const [loggedIs, setLoggedin] = useState<boolean>(isLoggedIn());

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handleSubmit = async () => {
    if (email.length > 2 && password.length > 2) {
      await login({email, password});
      setLoggedin(isLoggedIn());
    }
  };

  const handleLogout = async () => {
    await logout();
    setLoggedin(isLoggedIn());
  };

  return (
    <div>
      {!loggedIs ? (
        <div>
          <div>
            <label>
              Email:
              <input type="email" value={email} onChange={handleEmailChange} />
            </label>
          </div>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={handlePasswordChange}
            />
          </label>
          <div />
          <div>
            <button onClick={handleSubmit}>Sumit</button>
          </div>
        </div>
      ) : (
        <div>
          <div>Logged In</div>
          <button onClick={handleLogout}>Log out</button>
        </div>
      )}
    </div>
  );
};

export default Login;
