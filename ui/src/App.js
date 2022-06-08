import './App.css';
import { useEffect, useState } from "react";
import LineChart from './components/LineChart';

function App() {
  const [gameweeks, setGameweeks] = useState(null);

  useEffect(() => {
    console.log('gameweeks = ', gameweeks);
  }, [gameweeks])

  const readJsonFile = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileReader = new FileReader();
      fileReader.onload = ((e) => {
        const data = fileReader.result;
        const json = JSON.parse(data);

        if (json) {
          setGameweeks(json);
        }
      });
      fileReader.readAsText(file);
    }
  };

  const getRandomColor = () => {
    const min = 0;
    const max = 255;
    const randomBetween = (min, max) => min + Math.floor(Math.random() * (max - min + 1));

    return `rgb(${randomBetween(min, max)}, ${randomBetween(min, max)}, ${randomBetween(min, max)})`;
  }

  const getUserDataset = (user, data) => ({
    label: user.name,
    data: data,
    borderColor: user.lineColor,
    backgroundColor: user.lineColor
  })

  let users;
  const userGameweekPointsDictionary = {}; // user_id = key, value = array of gameweek_data.

  if (gameweeks) {
    // get list of users from final gameweek, as initial gameweeks may have fewer users.
    users = gameweeks[37].gameweek_data.map(g => ({ id: g.user_id, name: g.user, teamName: g.team_name, lineColor: getRandomColor() }));

    for (const gameweek of gameweeks) {
      for (const gameweekDataItem of gameweek.gameweek_data) {
        if (userGameweekPointsDictionary[gameweekDataItem.user_id]) {
          userGameweekPointsDictionary[gameweekDataItem.user_id].push({ points: gameweekDataItem.total_points, position: gameweekDataItem.rank });
        } else {
          userGameweekPointsDictionary[gameweekDataItem.user_id] = [{ points: gameweekDataItem.total_points, position: gameweekDataItem.rank }];
        }
      }
    }
  }

  let pointsLineChart;
  let positionsLineChart;
  let individualLineCharts;

  if (users) {
    pointsLineChart = (
        <LineChart
            chartTitle="TMSUK PREMIERSHIP 2021-22 Overall Points"
            datasets={users.map(u => getUserDataset(u, userGameweekPointsDictionary[u.id].map(x => x.points)))}
        />
    );

    positionsLineChart = (
        <LineChart
            chartTitle="TMSUK PREMIERSHIP 2021-22 Position changes"
            datasets={users.map(u => getUserDataset(u, userGameweekPointsDictionary[u.id].map(x => x.position)))}
            yAxis={{
              ticks: {
                min: 1,
                max: users.length,
                stepSize: 1,
                reverse: true
              }
            }}
        />
    );

    individualLineCharts = users.map(u => {
      return (
        <div>
          <LineChart chartTitle={`TMSUK PREMIERSHIP 2021-22 ${u.name} Points`} datasets={[getUserDataset(u, userGameweekPointsDictionary[u.id].map(x => x.points))]} />
          <LineChart
              chartTitle={`TMSUK PREMIERSHIP 2021-22 ${u.name} Position changes`}
              datasets={[getUserDataset(u, userGameweekPointsDictionary[u.id].map(x => x.position))]}
              yAxis={{
                ticks: {
                  min: 1,
                  max: users.length,
                  stepSize: 1,
                  reverse: true
                }
              }}
          />
        </div>
      );
    });
  }

  return (
    <div className="App">
      <div>
        <label htmlFor="file">Load Json gameweeks file</label>
        <input type="file" accept="application/json" id="file" onChange={readJsonFile} />
      </div>
      {pointsLineChart}
      {positionsLineChart}
      {individualLineCharts}
    </div>
  );
}

export default App;
