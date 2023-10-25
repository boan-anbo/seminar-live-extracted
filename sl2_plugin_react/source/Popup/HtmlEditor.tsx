// import * as React from 'react';
// import CKEditor from '@ckeditor/ckeditor5-react';
// import ClassicEditor from '@ckeditor/ckeditor5-build-classic'
import React from "react";
import {CKEditor} from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import './HtmlEditor.scss'

export interface HtmlEditorProps {
      data: string;
  onReady: (editor) => void;
  onChange: (event, editor) => void;
  onBlur: (event, editor) => void;
  onFocus: (event, editor) => void;
}


const HtmlEditor = (props: HtmlEditorProps): JSX.Element => {
  const {data, onReady, onChange, onBlur, onFocus} = props;
  return (
    <CKEditor
      editor={ClassicEditor}
      data={data}
      onReady={onReady}
      onChange={onChange}
      onBlur={onBlur}
      onFocus={onFocus}
    />
  );
};

export default HtmlEditor;
