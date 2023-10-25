import * as React from 'react';
import {useEffect, useRef, useState} from 'react';
import {FileDrop} from 'react-file-drop';
import {postLead, postSource} from '../functions/api';
import {getTabUrl} from '../functions/tabs';
import {getCurrentDomHtml} from '../functions/dom';
import './PostLeadPage.scss';
// import HtmlEditor from "./HtmlEditor";
import DescriptionEditor from './DescriptionEditor';
import HtmlEditor from './HtmlEditor';
import {isLoggedIn} from '../functions/auth';
import {
  getAllFilterDtoFromBackground,
  getAllFiltersFromBackground,
  getSelectedFilterFromBackground,
  setSelectedFilterToBackground,
} from '../functions/filters';
import {Organization} from '../models/organization';
import {Lead} from '../interfaces/lead';
import {Source} from '../models/source';
import {sortByPropertyName, titleCase} from '../functions/utils';
import {readFromClipboard} from '../functions/clipbaord';

const PostLeadPage: React.FC = () => {
  const [activeUrl, setActiveUrl] = useState<string>('');
  const [selectedOrgId, setSelectedHostOrgId] = useState<string>('');
  const [url, setUrl] = useState<string>('');
  const [posted, setPosted] = useState<boolean>(false);
  const [text, setText] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [html, setHtml] = useState<string>('');
  const [allOrganizations, setAllOrganizations] = useState<Organization[]>([]);
  const [startDateTimeString, setStartDateTimeString] = useState<string>();
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [
    eventbriteOrganizerName,
    setEventbriteOrganizerName,
  ] = useState<string>('');

  // file uploader
  const fileInputRef = useRef(null);

  const onFileInputChange = (event) => {
    const files = event.target.files as FileList;
    // do something with your files...
    const firstFile = files[0];
    setFile(firstFile);
  };

  const onTargetClick = () => {
    // @ts-ignore
    fileInputRef.current?.click();
  };

  const isTextValid = () => text.length > 2;
  const isUrlValid = () => url.length > 2;
  // const isHtmlValid = () => html.length > 2;
  const isFileValid = () => file !== null;
  const isLeadValid = () => isUrlValid() || isTextValid() || isFileValid();

  const handlePostLead = async () => {
    if (!isLeadValid() && !html) return;

    try {
      setErrorMessage('');
      const leadToPost: Lead = {};
      leadToPost.url = isUrlValid() ? url : activeUrl;
      leadToPost.text = text;
      leadToPost.html = html;
      leadToPost.startDateTimeString = startDateTimeString;
      if (file) {
        leadToPost.file = file;
      }
      leadToPost.hostOrganizations =
        selectedOrgId.length > 0 ? [selectedOrgId] : [];
      const result = await postLead(leadToPost);

      if (result) {
        setPosted(true);
      }
      console.log('Post Result');
    } catch (e) {
      console.log({e});
      if (e.response.status === 400) {
        setErrorMessage(e.response.data.url);
      }
    }
  };

  const handlePostEventbriteSource = async () => {
    if (!isLeadValid() && !html) return;

    try {
      const sourceToPost: Source = new Source();
      sourceToPost.url = isUrlValid() ? url : activeUrl;
      sourceToPost.sourceType = 'EVENTBRITE';
      sourceToPost.name = eventbriteOrganizerName;
      if (selectedOrgId) {
        sourceToPost.organizationId = selectedOrgId;
      }
      const result = await postSource(sourceToPost);

      if (result) {
        setPosted(true);
      }
      console.log('Post Source Result');
    } catch (e) {
      console.log({e});
      if (e.response.status === 400) {
        setErrorMessage(e.response.data.url);
      }
    }
  };

  const clearOrganization = () => {
    setSelectedHostOrgId('');
    setSelectedFilterFromLocalToBackground('');
  };
  const loadCurrentPageUrl = async () => {
    const domHtml = await getCurrentDomHtml();
    setHtml(domHtml);
    setUrl(activeUrl);

    if (activeUrl.toUpperCase().includes('EVENTBRITE')) {
      const result = activeUrl.match(/o\/(.*-[0-9]*)/g);
      if (result && result?.length > 0) {
        const slug = result[0];

        // @ts-ignore
        const name = titleCase(slug.split('-').join(' ').replace('o/', ''));
        setEventbriteOrganizerName(name);
      } else {
        setEventbriteOrganizerName('');
      }
    }

    // const result = await handlePostLead(domHtml);
    console.log('Current Page Loaded');
  };

  const loadAndPostCurrentPageUrl = async () => {
    await loadCurrentPageUrl();
    setTimeout(async () => handlePostLead(), 1000);
  };

  const clearURLandHTML = async () => {
    setHtml('');
    setUrl('');
  };

  const loadAllFiltersFromBackground = async () => {
    const filtersDto = await getAllFilterDtoFromBackground();
    console.log('Popup Received Filters Dto', filtersDto);
    // const sortedOrganization = sortByPropertyName(filtersDto.organizations, {sort})
    setAllOrganizations(filtersDto.organizations);
    console.log(filtersDto);
  };

  const getSelectedFilterName = () => {
    if (selectedOrgId && allOrganizations) {
      const orgName = allOrganizations.find((org) => org?.id === selectedOrgId)
        ?.name;
      return orgName ?? '';
    }
    return '';
  };
  const loadSelectedFilter = async () => {
    const selectedFilter = await getSelectedFilterFromBackground();
    if (selectedFilter) {
      setSelectedHostOrgId(selectedFilter.entityId_Value);
    }
  };

  const setLocalSelectedOrganization = (event) => {
    setSelectedHostOrgId(event.target.value);
    setSelectedFilterFromLocalToBackground(event.target.value);
  };

  const setSelectedFilterFromLocalToBackground = async (filterId: string) => {
    await setSelectedFilterToBackground(filterId);
  };

  useEffect(() => {
    async function updateUrl() {
      const tabUrl = await getTabUrl();
      setActiveUrl(tabUrl);
    }
    updateUrl();
    loadAllFiltersFromBackground().then(() => loadSelectedFilter());


  }, []);

  useEffect(() => {
    loadCurrentPageUrl();
  }, [activeUrl]);

  // const test = async () => {
  //   // const url = await getTabUrl()
  //   // alert(url)
  // };

  return (
    <section id="post_lead">
      <h2>Post Lead</h2>
      <div>Selected Filter Id: {selectedOrgId}</div>

      <div>
        <button onClick={clearOrganization}>Clear Organization</button>

        {allOrganizations?.length > 0 && (
          <label>
            Pick a school
            <select
              name="schools"
              value={selectedOrgId}
              onChange={setLocalSelectedOrganization}
            >
              {allOrganizations.map((organization, index) => {
                return (
                  <option key={organization.id} value={organization?.id}>
                    {organization?.name}
                  </option>
                );
              })}
            </select>
          </label>
        )}
      </div>

      {/* {text} */}
      <div>
        <button onClick={clearURLandHTML}>Clear URL and HTML</button>
        <button onClick={loadCurrentPageUrl}>Load Current Page</button>
        <span>{activeUrl}</span>
        <button onClick={loadAndPostCurrentPageUrl}>
          Load & Post Current Page
        </button>
      </div>

      {/* Post */}
      <div>{!isLoggedIn() ? 'YOU NEED TO LOGIN FIRST TO POST' : ''}</div>
      <button
        disabled={!isLeadValid() || !isLoggedIn()}
        onClick={handlePostLead}
      >
        <span style={{fontSize: '20px'}}>Post</span>
      </button>

      {/* Post Source */}

      <div>
        <div style={{marginTop: '20px'}}>
          {!isLoggedIn() ? 'YOU NEED TO LOGIN FIRST TO POST' : ''}
        </div>

        <button
          disabled={!isLeadValid() || !isLoggedIn()}
          onClick={handlePostEventbriteSource}
        >
          <span style={{fontSize: '20px'}}>Post Eventbrite Source</span>
        </button>
      </div>

      <div>
        <h2 style={{color: 'blue'}}>{eventbriteOrganizerName}</h2>
        <h2 style={{color: 'red'}}>{getSelectedFilterName()}</h2>
        <h2>{posted ? 'Lead Posted' : 'ready to post'}</h2>
        <h2 style={{color: 'red'}}>
          {errorMessage.length > 0 ? errorMessage : ''}
        </h2>
      </div>
      {/* Number input */}
      <div>
        <div>Start Date Time String</div>

        <input
          type="text"
          autoFocus
          value={startDateTimeString}
          onChange={(e) => setStartDateTimeString(e.target.value)}
        />
        <div>
          <h2>Start Date Time String </h2>
          <h2 style={{color: "blue"}}>{startDateTimeString}</h2>
        </div>

        <div>
          <h2>URL </h2>
          <h3 style={{color: "green"}}>{url}</h3>
        </div>
      </div>

      <div>
        <label>
          Url:
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </label>
      </div>
      <div>
        <input
          onChange={onFileInputChange}
          ref={fileInputRef}
          type="file"
          className="hidden"
        />

        <FileDrop onTargetClick={onTargetClick} />
      </div>
      <div>
        <h3>Description</h3>
        <DescriptionEditor
          data={text}
          onReady={(editor) => {
            // You can store the "editor" and use when it is needed.
            console.log('Editor is ready to use!', editor);
          }}
          onChange={(event, editor) => {
            const data = editor.getData();
            console.log({event, editor, data});
            setText(data);
          }}
          onBlur={(event, editor) => {
            console.log('Blur.', editor);
          }}
          onFocus={(event, editor) => {
            console.log('Focus.', editor);
          }}
        />
      </div>
      <div>
        <h3>Html</h3>
        <HtmlEditor
          data={html}
          onReady={(editor) => {
            // You can store the "editor" and use when it is needed.
            console.log('Editor is ready to use!', editor);
          }}
          onChange={(event, editor) => {
            const data = editor.getData();
            console.log({event, editor, data});
            setHtml(data);
          }}
          onBlur={(event, editor) => {
            console.log('Blur.', editor);
          }}
          onFocus={(event, editor) => {
            console.log('Focus.', editor);
          }}
        />
      </div>
    </section>
  );
};

export default PostLeadPage;
