import React, { useState } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

/**
 * React TypeScript 组件示例
 * 用户信息展示组件
 */
function UserProfile({ user }: { user: User }) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="user-profile">
      <h3>{user.name}</h3>
      <p>邮箱: {user.email}</p>
      <button onClick={() => setIsEditing(!isEditing)}>
        {isEditing ? '保存' : '编辑'}
      </button>
    </div>
  );
}

export default UserProfile;