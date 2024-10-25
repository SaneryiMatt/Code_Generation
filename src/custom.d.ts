// src/custom.d.ts
import React from 'react';

declare module 'react' {
  interface InputHTMLAttributes<T> {
    webkitdirectory?: boolean; // 允许使用 webkitdirectory 属性
  }
}
