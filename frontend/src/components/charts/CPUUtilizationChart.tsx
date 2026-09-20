import {
  Area,
  AreaChart,
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type {
  CPUHistoryPoint,
} from '../../types/recommendations'

interface CPUUtilizationChartProps {
  data: CPUHistoryPoint[]
}

function CPUUtilizationChart({
  data,
}: CPUUtilizationChartProps) {
  const chartData = data.map((point) => ({
    timestamp: point.timestamp,
    cpu: point.average_cpu_percent,
    label: new Date(
      point.timestamp,
    ).toLocaleString([], {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
    }),
  }))

  if (chartData.length === 0) {
    return null
  }

  return (
    <div className="cpu-chart">
      <div className="cpu-chart-header">
        <div>
          <span>
            CPU UTILIZATION HISTORY
          </span>

          <p>
            Hourly average · Last 7 days
          </p>
        </div>

        <div className="chart-threshold">
          <span />
          5% threshold
        </div>
      </div>

      <div className="cpu-chart-container">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <AreaChart
            data={chartData}
            margin={{
              top: 10,
              right: 8,
              left: -20,
              bottom: 0,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#172233"
            />

            <XAxis
              dataKey="label"
              tick={{
                fill: '#536983',
                fontSize: 9,
              }}
              tickLine={false}
              axisLine={false}
              minTickGap={40}
            />

            <YAxis
              tick={{
                fill: '#536983',
                fontSize: 9,
              }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) =>
                `${value}%`
              }
              domain={[
                0,
                (dataMax: number) =>
                  Math.max(
                    Math.ceil(dataMax * 1.2),
                    6,
                  ),
              ]}
            />

            <Tooltip
              contentStyle={{
                background: '#0d1624',
                border: '1px solid #203047',
                borderRadius: '8px',
                fontSize: '11px',
              }}
              labelStyle={{
                color: '#8ea4c2',
              }}
              formatter={(value) => [
                `${Number(value).toFixed(2)}%`,
                'CPU',
              ]}
            />

            <ReferenceLine
              y={5}
              stroke="#f59e0b"
              strokeDasharray="5 5"
            />

            <Area
              type="monotone"
              dataKey="cpu"
              stroke="#5b8cff"
              fill="#5b8cff"
              fillOpacity={0.12}
              strokeWidth={2}
              dot={false}
              activeDot={{
                r: 3,
              }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default CPUUtilizationChart