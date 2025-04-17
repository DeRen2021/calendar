import React from 'react';
import { FaGithub } from "react-icons/fa";

const Navbar: React.FC = () => {
  return (
    // 添加 fixed top-0 w-full z-50 使其固定在顶部并覆盖内容
    <nav className="fixed top-0 w-full z-50 flex justify-between items-center bg-gray-100 py-2 px-4 border-b border-gray-200">
      {/* 左侧 Brand */}
      <div>
        <a href="/" className="text-xl font-bold text-gray-800 no-underline">Schedule with De Ren</a>
      </div>

      {/* 右侧内容容器 (链接 + GitHub 图标) */}
      <div className="flex items-center">
        {/* 现有导航链接 */}
        <ul className="flex list-none p-0 m-0">
          <li className="ml-4">
            <a href="/about" className="text-blue-600 no-underline hover:underline">关于</a>
          </li>
          <li className="ml-4">
            <a href="/contact" className="text-blue-600 no-underline hover:underline">联系我们</a>
          </li>
        </ul>

        {/* GitHub 图标链接 (新添加) */}
        <a
            href="https://github.com/你的用户名/你的项目"
            target="_blank"
            rel="noopener noreferrer"
            className="ml-6 text-gray-700 hover:text-gray-900"
            aria-label="GitHub Repository"
            >
            <FaGithub className="w-6 h-6" />
        </a>
      </div>
    </nav>
  );
};

export default Navbar; 