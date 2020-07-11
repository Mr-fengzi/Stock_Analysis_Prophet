from stock_analysis import *
import fbprophet
from fbprophet.plot import add_changepoints_to_plot


def data_preprocess(df):
    data = df['Close'].reset_index()
    data = data.rename(columns={'Date': 'ds', 'Close': 'y'})
    return data

def model_prophet1(data):
    model = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=True)
    # 定义模型
    model.fit(data)  # 训练模型
    forecast_df = model.make_future_dataframe(periods=365, freq='D')  # 生成需预测序列
    forecast = model.predict(forecast_df)  # 模型预测
    model.plot(forecast, xlabel='Date', ylabel='Close Price ¥')  # 绘制预测图
    plt.title('Close Price of 000001.SZ')
    plt.show()

    fig = model.plot(forecast)  # 绘制预测图
    a = add_changepoints_to_plot(fig.gca(), model, forecast)  # 增加变化点

def plot(m, fcst, ax=None, uncertainty=True, plot_cap=True, xlabel='ds',
         ylabel='y', plot_color='#0072B2'):
    """Plot the Prophet forecast.
   Parameters
   ----------
   m: Prophet model.
   fcst: pd.DataFrame output of m.predict.
   ax: Optional matplotlib axes on which to plot.
   uncertainty: Optional boolean to plot uncertainty intervals.
   plot_cap: Optional boolean indicating if the capacity should be shown

 in the figure, if available.
   xlabel: Optional label name on X-axis
   ylabel: Optional label name on Y-axis
   Returns
   -------
   A matplotlib figure.
   """
    if ax is None:
        fig = plt.figure(facecolor='w', figsize=(10, 6))
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    fcst_t = fcst['ds'].dt.to_pydatetime()
    ax.plot(m.history['ds'].dt.to_pydatetime(), m.history['y'], 'k.')
    ax.plot(fcst_t, fcst['yhat'], ls='-', c=plot_color)
    if 'cap' in fcst and plot_cap:
        ax.plot(fcst_t, fcst['cap'], ls='--', c='k')
    if m.logistic_floor and 'floor' in fcst and plot_cap:
        ax.plot(fcst_t, fcst['floor'], ls='--', c='k')
    if uncertainty:
        ax.fill_between(fcst_t, fcst['yhat_lower'], fcst['yhat_upper'],
                        color=plot_color, alpha=0.2)
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig

def model_prophet2(data):
    fig, ax = plt.subplots(figsize=(16, 9))
    # 此处代码运行时间较长,请耐心等待
    for point, color in zip([0.01, 0.05, 0.1], ['blue', 'red', 'yellow']):
        temp_model = fbprophet.Prophet(changepoint_prior_scale=point,
                                       daily_seasonality=True)
        temp_model.fit(data)
        forecast = temp_model.make_future_dataframe(periods=365 * 2, freq='D')  # 2 年
        forecast = temp_model.predict(forecast)
        plot(temp_model, forecast, ax=ax, xlabel='Date', ylabel='Close Price ¥',
             plot_color=color)
        plt.show()



if __name__ == '__main__':
    StockNum = '000001.SZ'
    df = get_StockBata_byCache(StockNum)
    data = data_preprocess(df)
    # model_prophet1(data)
    model_prophet2(data)