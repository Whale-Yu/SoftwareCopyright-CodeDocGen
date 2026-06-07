import React, { useState } from 'react';

/**
 * React 组件示例
 * 简单的计数器组件
 */
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div className="counter">
      <h2>计数器: {count}</h2>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
      <button onClick={() => setCount(count - 1)}>
        减少
      </button>
    </div>
  );
}

export default Counter;