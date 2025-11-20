<template>
  <div class="page-container">
    <nvabar />
    <div class="sidebar">
      <ul class="relation-list">
        <li
          v-for="relation in relationList"
          :key="relation.value"
          class="relation-item"
          :class="{ active: selectedRelation === relation.value }"
          @click="handleRelationClick(relation.value)"
        >
          <h2>{{ relation.label }}</h2>
          <p class="desc">{{ relation.desc }}</p>
        </li>
      </ul>
    </div>
    <div class="control-panel">
      <button class="ctrl-btn" @click="zoomIn" title="放大">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="16" />
          <line x1="8" y1="12" x2="16" y2="12" />
        </svg>
      </button>
      <button class="ctrl-btn" @click="zoomOut" title="缩小">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" />
          <line x1="8" y1="12" x2="16" y2="12" />
        </svg>
      </button>
      <button class="ctrl-btn" @click="resetView" title="居中">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" />
          <circle cx="12" cy="12" r="4" fill="currentColor" />
        </svg>
      </button>
    </div>
    <div class="search-bar">
      <label for="searchID" class="search-label">疾病搜索词：</label>
      <input
        id="searchID"
        type="text"
        placeholder="例如：感冒"
        v-model="diseaseKeyword"
        @keyup.enter="handleSearch"
        class="search-input"
      />
      <button class="search-btn" @click="handleSearch">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        搜索
      </button>
    </div>
    <div class="graph-wrapper">
      <div id="allmap" class="graph-container" ref="chart">
        <div v-if="links.length && nodeCount===0 && edgeCount===0" class="tip-none-other">
          <h2>节点数量为空</h2>
        </div>
        <div v-if="!links.length" class="tip-none">
          <h2>暂无数据</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import Nvabar from './nvabar.vue';

export default {
  name: 'MedicalNeo4jGraph',
  components: { Nvabar },
  data() {
    return {
      diseaseKeyword: '',
      selectedRelation: 'show_all',
      relationList: [
        { value: 'show_all', label: '显示全部', desc: '显示全部节点' },
        { value: 'acompany_with', label: '伴随', desc: '显示会伴随的疾病' },
        { value: 'belongs_to', label: '属于', desc: '显示属于的疾病' },
        { value: 'common_drug', label: '常用药物', desc: '显示所需药物' },
        { value: 'do_eat', label: '宜食', desc: '显示宜食的食物' },
        // { value: 'drugs_of', label: '药物', desc: '显示药物的相关信息' },
        { value: 'has_symptom', label: '有症状', desc: '显示有症状的疾病' },
        { value: 'need_check', label: '需要检查', desc: '显示需要检查的项目' },
        { value: 'no_eat', label: '忌食', desc: '显示忌食的食物' },
        { value: 'recommand_drug', label: '推荐药物', desc: '显示推荐的药物' },
        { value: 'recommand_eat', label: '推荐饮食', desc: '显示推荐的饮食' }
      ],
      nodeCount: 0,
      edgeCount: 0,
      links: [],
      nodes: {},
      svg: null,
      d3Elements: {},
      zoom: null,
      relationshipMap: {
        'acompany_with': '伴随',
        'belongs_to': '属于',
        'common_drug': '常用药物',
        'do_eat': '宜食',
        //'drugs_of': '药物',
        'has_symptom': '有症状',
        'need_check': '需要检查',
        'no_eat': '忌食',
        'recommand_drug': '推荐药物',
        'recommand_eat': '推荐饮食'
      }
    };
  },
  mounted() {
    const searchTerm = this.$route.query.search_term;
    if (searchTerm) {
      this.diseaseKeyword = searchTerm;
      this.fetchGraphData();
      this.$nextTick(() => setTimeout(() => this.highlightNode(searchTerm), 800));
    } else {
      this.fetchGraphData();
    }
  },
  methods: {
    async fetchGraphData() {
      const search = this.diseaseKeyword.trim();
      try {
        const { data } = await axios.get(`/api/view?search_term=${encodeURIComponent(search)}`);
        this.links = data || [];
      } catch (e) {
        console.error(e);
      }
      this.renderGraph();
    },
    handleSearch() {
      this.fetchGraphData();
    },
    handleRelationClick(val) {
      this.selectedRelation = val;
      if (val === 'show_all') this.toggleAll();
      else this.toggleRelationship(val);
    },
    zoomIn() {
      this.zoom.scaleBy(this.svg.transition().duration(300), 1.3);
    },
    zoomOut() {
      this.zoom.scaleBy(this.svg.transition().duration(300), 0.7);
    },
    resetView() {
      this.svg.transition().duration(500).call(
        this.zoom.transform,
        d3.zoomIdentity.translate(-800, -600).scale(1)
      );
    },
    renderGraph() {
      // 清空原有svg
      if (this.svg) {
        this.svg.remove();
      }
      this.nodes = {};
      this.links.forEach(link => {
        link.source = this.nodes[link.source] || (this.nodes[link.source] = { name: link.source });
        link.target = this.nodes[link.target] || (this.nodes[link.target] = { name: link.target });
      });
      const width = 3000, height = 1800;
      // 绿色简约配色
      const colorList = ["#40c057", "#2da143", "#b9e7c3", "#d4f0d9", "#ebfbee", "#8b4513", "#a3e635", "#bef264", "#bbf7d0", "#22c55e"];
      const color = i => colorList[i % colorList.length];
      const nodesArr = Object.values(this.nodes);
      const linksArr = this.links.map(l => ({...l, source: l.source, target: l.target}));
      // d3-force模拟，减小排斥力，节点分布更轻松
      const simulation = d3.forceSimulation(nodesArr)
        .force("link", d3.forceLink(linksArr).distance(220).id(d => d.name))
        .force("charge", d3.forceManyBody().strength(-350))
        .force("center", d3.forceCenter(width / 2, height / 2));
      // 支持缩放和平移
      this.svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("width", width)
        .attr("height", height);
      this.zoom = d3.zoom()
        .scaleExtent([0.2, 2])
        .on("zoom", function (event) {
          g.attr("transform", event.transform);
        });
      this.svg.call(this.zoom);
      // 主g容器
      const g = this.svg.append("g");
      // 边
      const edges_line = g.append('g')
        .attr('class', 'edges')
        .selectAll(".edgepath")
        .data(linksArr)
        .enter()
        .append("line")
        .attr("stroke", "#40c057")
        .attr("stroke-width", 2);
      // 边文本
      const edges_text = g.append("g")
        .attr('class', 'edge-text')
        .selectAll(".edgelabel")
        .data(linksArr)
        .enter()
        .append("text")
        .attr("font-size", 18)
        .attr("fill", "#22c55e")
        .text(d => this.relationshipMap[d.rela] || '');
      // 节点
      const circle = g.append("g").selectAll("circle")
        .data(nodesArr)
        .enter().append("circle")
        .attr("r", 28)
        .attr("fill", (d, i) => color(i))
        .attr("stroke", "#fff")
        .attr("stroke-width", 3)
        .style("cursor", "pointer")
        // .on("dblclick", node => this.navigateToNode(node.name))
        .on("mouseover", function () { d3.select(this).attr("r", 34); })
        .on("mouseout", function () { d3.select(this).attr("r", 28); })
        .call(d3.drag()
          .on("start", function(event, d) {
            if (!event.active) simulation.alphaTarget(0.2).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", function(event, d) {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", function(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
        );
      // 节点文本
      const text = g.append("g").selectAll("text.node-label")
        .data(nodesArr)
        .enter()
        .append("text")
        .attr("class", "node-label")
        .attr("font-size", 18)
        .attr("fill", "#1e293b")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .text(d => d.name);
      // tick函数
      simulation.on("tick", () => {
        circle.attr("cx", d => d.x = Math.max(40, Math.min(width - 40, d.x)))
              .attr("cy", d => d.y = Math.max(40, Math.min(height - 40, d.y)));
        text.attr("x", d => d.x)
            .attr("y", d => d.y + 6);
        edges_line.attr("x1", d => d.source.x)
                  .attr("y1", d => d.source.y)
                  .attr("x2", d => d.target.x)
                  .attr("y2", d => d.target.y);
        edges_text.attr("x", d => (d.source.x + d.target.x) / 2)
                  .attr("y", d => (d.source.y + d.target.y) / 2 - 10);
        this.updateCounts();
      });
      // 保存d3元素引用
      this.d3Elements = { circle, text, edges_line, edges_text };
      this.updateCounts();
    },
    navigateToNode(nodeName) {
      window.open("https://baike.baidu.com/item/" + nodeName, "_blank");
    },
    toggleRelationship(relationship) {
      const { edges_line, edges_text, circle, text } = this.d3Elements;
      // 找到相关边
      const relatedEdges = edges_line.filter(d => d.rela === relationship);
      // 相关节点
      const relatedNodes = new Set();
      relatedEdges.each(edge => {
        relatedNodes.add(edge.source.name);
        relatedNodes.add(edge.target.name);
      });
      // 隐藏所有
      edges_line.style("display", "none");
      edges_text.style("display", "none");
      circle.style("display", "none");
      text.style("display", "none");
      // 显示相关边
      relatedEdges.style("display", "inline");
      // 显示相关边的文本
      edges_text.filter(function(d) {
        return relatedEdges.filter(function(edge) {
          return edge.source === d.source && edge.target === d.target;
        }).size() > 0;
      }).style("display", "inline");
      // 显示相关节点
      circle.filter(d => relatedNodes.has(d.name)).style("display", "inline");
      text.filter(d => relatedNodes.has(d.name)).style("display", "inline");
      this.updateCounts();
      console.log(`节点数量: ${this.nodeCount},关系边数量: ${this.edgeCount}`)
    },
    toggleAll() {
      const { edges_line, edges_text, circle, text } = this.d3Elements;
      const isHidden = edges_line.style("display") === "none";
      const newDisplayState = isHidden ? "inline" : "none";
      edges_line.style("display", newDisplayState);
      edges_text.style("display", newDisplayState);
      circle.style("display", newDisplayState);
      text.style("display", newDisplayState);
      this.updateCounts();
    },
    updateCounts() {
      const { circle, edges_line } = this.d3Elements;
      this.nodeCount = circle ? circle.filter(function() { return d3.select(this).style("display") !== "none"; }).size() : 0;
      this.edgeCount = edges_line ? edges_line.filter(function() { return d3.select(this).style("display") !== "none"; }).size() : 0;
    },
    highlightNode(nodeName) {
      // 高亮节点（绿色边框/放大）
      if (!this.d3Elements.circle) return;
      this.d3Elements.circle.each(function(d) {
        if (d.name === nodeName) {
          d3.select(this)
            .attr('stroke', '#22c55e')
            .attr('stroke-width', 8)
            .attr('r', 38);
        } else {
          d3.select(this)
            .attr('stroke', '#fff')
            .attr('stroke-width', 3)
            .attr('r', 28);
        }
      });
    }
  }
};
</script>

<style scoped lang="scss">
$page-bg: #f8fff9;
$primary: #40c057;
$primary-dark: #2da143;
$light: #f0fdf4;
$card-bg: #ffffff;
$text: #1e293b;
$border: #d4f0d9;

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.page-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: $page-bg;
  font-family: "微软雅黑", sans-serif;
}

/* ---------- 左侧关系列表 ---------- */
.sidebar {
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  width: 240px;
  // background: $card-bg;
  background-color: #ecf9ee;
  border-right: 1px solid $border;
  padding: 2rem 1.5rem;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 2px 0 12px rgba(64, 192, 87, .08);
}

/* 滚动条样式 */
.sidebar::-webkit-scrollbar {
  width: 0.7rem;
}

.sidebar::-webkit-scrollbar-track {
  background-color: #ecf9ee;
  border-radius: 0.4rem;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: #c6eccd;
  border-radius: 0.4rem;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background-color: #b3e6bc;
}

.relation-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  position: absolute;
}

.relation-item {
  background: $light;
  border: 2px solid transparent;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  transition: all .25s ease;
  box-shadow: 0 2px 8px rgba(64, 192, 87, .06);

  &.active,
  &:hover {
    background: #d4f0d9;
    border-color: $primary;
    transform: translateY(-2px);
  }

  h2 {
    font-size: 1.1rem;
    color: $text;
    font-weight: 600;
    margin-bottom: 6px;
  }

  .desc {
    font-size: 0.92rem;
    color: #555;
    line-height: 1.5;
  }
}

/* ---------- 右侧控制面板 ---------- */
.control-panel {
  position: fixed;
  right: 24px;
  top: 80%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 100;
}

.ctrl-btn {
  width: 48px;
  height: 48px;
  background: $card-bg;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, .1);
  transition: all .2s;

  svg {
    width: 20px;
    height: 20px;
    color: $primary;
  }

  &:hover {
    background: $primary;

    svg {
      color: #fff;
    }

    transform:scale(1.1);
  }
}

/* ---------- 底部搜索栏 ---------- */
.search-bar {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 28px;
  // background: linear-gradient(135deg, $primary, $primary-dark);
  background: #40c057;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(64, 192, 87, .25);
  z-index: 100;

  .search-label {
    color: #fff;
    font-weight: 700;
    font-size: 1rem;
    white-space: nowrap;
  }

  .search-input {
    padding: 12px 20px;
    width: 200px;
    border: none;
    border-radius: 16px;
    font-size: 1rem;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, .08);
    transition: width .3s;

    &:focus {
      width: 260px;
    }
  }

  .search-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 24px;
    background: #fff;
    color: $primary;
    border: none;
    border-radius: 20px;
    font-weight: 600;
    cursor: pointer;
    transition: all .2s;
    box-shadow: 0 4px 12px rgba(0, 0, 0, .1);

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: #f0fdf2;
      transform: translateY(-1px);
    }
  }
}

/* ---------- 图谱容器 ---------- */
.graph-wrapper {
  margin-left: 300px;
  height: 100vh;
  position: relative;
  overflow: hidden;
  background: $page-bg;
}

.graph-container {
  width: 100%;
  height: 100%;
}

/* ---------- 提示文字 ---------- */
.tip-none,
.tip-none-other {
  position: absolute;
  top: 50%;
  left: 43%;
  transform: translate(-50%, -50%);

  h2 {
    color: $primary;
    font-size: 28px;
    font-weight: 700;
    opacity: 0.6;
  }
}

/* ---------- D3 样式 ---------- */
svg circle {
  transition: r .2s;
  box-shadow: 0 2px 8px rgba(34, 230, 93, .15);
}

.edges line {
  stroke: $primary;
  stroke-width: 2;
}

.node-label {
  font-size: 20px;
  fill: $text;
  font-weight: bold;
  text-anchor: middle;
}
</style>