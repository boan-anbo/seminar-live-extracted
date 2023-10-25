import * as React from 'react';
import {useState} from 'react';
import {browser, Tabs} from 'webextension-polyfill-ts';

import './styles.scss';
import Webinars from './Webinars';
import {VIEWS} from '../interfaces/views';
import Login from './Login';
import Search from './Search';
import PostLeadPage from './PostLeadPage';

function openWebPage(url: string): Promise<Tabs.Tab> {
  return browser.tabs.create({url});
}

function sendMessageToBackground() {
  console.log('Sending message');
  browser.runtime.sendMessage('test');
}


function getView(view: VIEWS) {
  switch (view) {
    case VIEWS.LOGIN:
      return <Login />;
    case VIEWS.POST_LEAD:
      return <PostLeadPage />;
    case VIEWS.WEBINARS:
      return <Webinars />;
    case VIEWS.SEARCH:
      return <Search />;
    default:
      return <div> </div>;
  }
}

const Popup: React.FC = () => {
  const [tabId, setTabId] = useState('empty Id');
  const [view, setView] = useState(VIEWS.POST_LEAD);

  return (
    <section id="popup">
      <div className="nav-bar mx-2">
        <button onClick={() => setView(VIEWS.WEBINARS)}>Latest Webinars</button>
        <button onClick={() => setView(VIEWS.POST_LEAD)}>Post Load</button>
        <button onClick={() => setView(VIEWS.LOGIN)}>Login</button>
        <button onClick={() => setView(VIEWS.SEARCH)}>Search</button>
      </div>
      <div>{getView(view)}</div>
    </section>
  );
};

export default Popup;
