import math
import random
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pandas as pd
import plotly.express as px



#user inputs

# Lambda = 2.25
# mew = 8.98
# st1 = 7 #lb for gg service
# st2 = 5 #ub for gg service
# #mean for gg ia normal
# sigma = 1.5 #sigma for gg ia normal
# c = 2


A = 55
M = 1994
Z0 = 10112166
C = 9
a = 1
b = 3

def CP(Lambda):
    array = []
    i=1
    total = 0
    num_of_cust = 0
    while total != 1:
        total = 0 
        for x in range (0, i):
            temp = (pow(Lambda, x)) * math.exp(-Lambda) / math.factorial(x)
            total += temp
        array.append(total)
        i+=1
        num_of_cust+=1
    return array, num_of_cust

def CPlookUp(Lambda, num_of_cust):
    array = []
    for i in range (0, num_of_cust):
        total = 0
        for x in range (0, i):
            temp = (Lambda**x) * math.exp(-Lambda) / math.factorial(x)
            total += temp
        array.append(total)
    return array

def IAMM(CP, CPlo, num_of_cust):
    IA = []
    for j in range (1, num_of_cust):
        temp = random.random()
        for i in range (0, num_of_cust - 1):
            if (temp<CP[i] and temp>CPlo[i]):
                IA.append(i)
    return IA

def IAMG(CP, CPlo, num_of_cust, mew):
    IA = []
    while (len(IA)!=num_of_cust):
        temp = -mew * math.log(random.random())
        for i in range (0, num_of_cust - 1):
            if (temp<CP[i] and temp>CPlo[i]):
                IA.append(i)
    return IA

def IAGG(CP, CPlo, num_of_cust, mew):
    IA = []
    while (len(IA)!=num_of_cust):
        #temp = np.random.normal(mew, sigma)
        temp = -mew * math.log(random.random())
        for i in range (0, num_of_cust - 1):
            if (temp<CP[i] and temp>CPlo[i]):
                IA.append(i)
    return IA

def Arrivals(arrivals, IA, num_of_cust):
    temp = 0
    print(len(IA), num_of_cust)
    for i in range (0, num_of_cust - 1):
        temp += IA[i]
        arrivals.append(temp)

def ServiceMM(num_of_cust, mew):
    service = []
    for i in range (0, num_of_cust):
        temp = -mew * math.log(random.random())
        service.append(round(temp))
    return service

def ServiceMG(num_of_cust, mew, sigma):
    service = []
    for i in range (0, num_of_cust):
        temp = np.random.normal(mew, sigma)
        service.append(round(temp))
    return service

def ServiceGG(num_of_cust, st1, st2):
    service = []
    for i in range (0, num_of_cust):
        temp = (random.random()-st1)/(st2-st1)
        service.append(round(temp))
    return service

def generate_priority(A, M, Z0, C, a, b, num_of_cust):
    Z = [Z0]
    R = []
    RanNum = []
    GP =[]
    for i in range (0, num_of_cust):
        temp = (A*(Z[i])+C) % M
        Z.append(temp)
        R.append(Z[i+1])
        RanNum.append(R[i]/M)
        priority = a + RanNum[i] * (b - a)
        GP.append(round(priority))
    Z.remove(Z[-1])
    return Z, R, RanNum, GP


def qeueing(num_of_cust, arrivals, service):
  
  Z, R, RanNum, GP = generate_priority(A, M, Z0, C, a, b, num_of_cust)
  arrived = []
  labels = []
  for i in range(len(arrivals)):
        arrived.append({
        "name": f"Patient {i + 1}",
        "arrival_time": arrivals[i],
        "service_time": service[i],
        "priority": GP[i],
        })
        labels.append(f"Patient {i+1}")

  starts = []   
  width = []   
  table = PrettyTable([
    "Name", "Arrival Time", "Service Time", "Priority", "Service Start Time",
    "Service End Time", "Turnaround Time", "Wait Time", "Response Time"
        ])
  time = 0          #simulation clock intialised
  n = len(arrived)
  executed = 0
  current = 0
  waiting_queue = []
  executed_processes = set()
  remaining_times = {
      p["name"]: [p["service_time"], p["priority"], None, 0]
      for p in arrived
  }
  total_service_time = 0
  total_busy_time = 0

  while executed < n:
    for p in arrived:
      if p["arrival_time"] == time and p["name"] not in executed_processes:
        waiting_queue.append(p)

        if (not current) or (waiting_queue and remaining_times[p["name"]][1] < remaining_times[current["name"]][1]):
          if current:
            print(
                "\n"
                f"Leaving {current['name']} and Switching to process {p['name']} due to priority."
                "\n")
          current = p

    if not current and waiting_queue:
      current = min(waiting_queue, key=lambda x: remaining_times[x["name"]][1])

    if not current and not waiting_queue:
      print("\n"
            f"Time {time}: Server is idle."
            "\n")

    if current:
      print(f"Time {time}: Executing {current['name']}")

      if remaining_times[current["name"]][2] == None:
        remaining_times[current["name"]][2] = time  # Service start time

      if remaining_times[current["name"]][0] > 0:
        remaining_times[current["name"]][0] -= 1
        total_service_time += 1
        total_busy_time += 1

      if remaining_times[current["name"]][0] <= 0:
        executed_processes.add(current["name"])
        remaining_times[current["name"]][3] = time # Service end time
        waiting_queue = [
            p for p in waiting_queue if p["name"] != current["name"]
        ]

        turnaround_time = remaining_times[
            current["name"]][3] - current["arrival_time"]

        wait_time = max(turnaround_time - current["service_time"], 0)

        response_time = remaining_times[
            current["name"]][2] - current["arrival_time"]

        table.add_row([
            current["name"], current["arrival_time"], current["service_time"],
            current["priority"], remaining_times[current["name"]][2],                   #table index 4 and 5 have start and end time respectively
            remaining_times[current["name"]][3], turnaround_time, wait_time,
            response_time
        ])
        width.append(remaining_times[current["name"]][3] - remaining_times[current["name"]][2])
        starts.append(remaining_times[current["name"]][2])
        current = None
        executed += 1
        
    # df = pd.DataFrame({
    #     'Task': labels,
    #     'Start': starts,
    #     'Finish': [starts[i] + width[i] for i in range(len(starts))],
    #     'Priority': [arrived[i]['priority'] for i in range(len(arrived))]
    # })

    time += 1
  server_utilization_rate = total_busy_time / time
#   plot_gantt_chart(starts, width, labels)


  print(table)
  generate_list = lambda n: list(range(n + 1))
  plt.barh(range(len(labels)), width, left=starts, tick_label=labels)
  print("\n")
  print(f"\nTotal Service Time: {total_service_time}")

  total_waiting_time = 0
  total_turnaround_time = 0
  total_response_time = 0

  for p in arrived:
    if p["name"] in executed_processes:
      turnaround_time = remaining_times[p["name"]][3] - p["arrival_time"]
      wait_time = max(turnaround_time - p["service_time"], 0)
      response_time = remaining_times[p["name"]][2] - p["arrival_time"]

      total_waiting_time += wait_time
      total_turnaround_time += turnaround_time
      total_response_time += response_time

  # Calculate averages
  average_waiting_time = total_waiting_time / n
  average_turnaround_time = total_turnaround_time / n
  average_response_time = total_response_time / n

  # Print the results
  print("\n")
  print(f"Average Waiting Time: {average_waiting_time:.2f}")
  print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
  print(f"Average Response Time: {average_response_time:.2f}")
  print(f"\nServer Utilization Rate: {server_utilization_rate * 100:.2f} %")

  return average_waiting_time, average_response_time, average_turnaround_time

def plot_gantt_chart(starts, width, labels, df):
    fig = px.timeline(
        df, x_start='Start', x_end='Finish', y='Task', color='Priority',
        labels={"Task": "Name"}
    )
    fig.update_yaxes(categoryorder='total ascending')  # Order tasks by Name
    fig.update_layout(
        title='Gantt Chart for Queueing Simulation',
        xaxis_title='Simulation Time',
        yaxis_title='Task',
        showlegend=False  # Hide legend for better readability
    )
    fig.show()


def calculate_p0(rho, c):
    numerator = pow(rho, c) / math.factorial(c)
    denominator = sum([(rho ** k) / math.factorial(k) for k in range(c)])
    pzero = 1 / (numerator + denominator)
    return pzero


def mmc(Lambda, mew, c):
    arrival_rate = Lambda
    service_rate = mew
    
    utilization = arrival_rate / (service_rate*c)
    p0 = calculate_p0(utilization, c)
    lq = p0*((Lambda/mew)**c)*utilization
    wq = lq / arrival_rate
    w = wq + (1/ service_rate)
    l = arrival_rate * w
    
    results = {
        'Utilization': utilization,
        'Probability of zero customers': p0,
        'Average number of customers in the system': l,
        'Average number of customers in the queue': lq,
        'Average waiting time in the system': w,
        'Average waiting time in the queue': wq
        }
    print(results)
    return lq, wq, l, w, utilization

def mgc(Lambda, mew, c):
    
    arrival_rate = Lambda
    service_rate = mew
    mean_arrival = 1/Lambda
    mean_service = 1/mew
    var_arrival = 1/Lambda**2
    var_service = 1/mew**2

    Ca2= var_arrival/((mean_arrival)**2)
    Cs2= var_service/((mean_service)**2)
    
    utilization = arrival_rate / (service_rate*c)
    p0 = calculate_p0(utilization, c)
    lq = p0*((Lambda/mew)**c)*utilization
    approx = (Ca2+Cs2)/2
    wq = (lq / arrival_rate)*(approx)
    w = wq + (1/ service_rate)
    l = arrival_rate * w
    
    results = {
        'Utilization': utilization,
        'Probability of zero customers': p0,
        'Average number of customers in the system': l,
        'Average number of customers in the queue': lq,
        'Average waiting time in the system': w,
        'Average waiting time in the queue': wq
        }
    print(results)
    return lq, wq, l, w, utilization

def ggc(Lambda, st1, st2, c, mew):
    arrival_rate = Lambda
    service_rate = mew

    mean_arrival = 1/Lambda
    mean_service = 1/((st1+st2)/2)
    var_arrival = (1/Lambda)**2
    var_service= ((st2 - st1)**2) / 12

    Ca2= var_arrival/(mean_arrival**2)
    Cs2= var_service/(mean_service**2)

    utilization = service_rate / (arrival_rate*c)
    p0 = calculate_p0(utilization, c)
    lq = p0*((Lambda/mew)**c)*utilization
    approx = (Ca2+Cs2)/2
    wq = (lq / arrival_rate)*(approx)
    w = wq + (1/ service_rate)
    l = arrival_rate * w

    results= {
        'Utilization': utilization,
        'Probability of zero customers': p0,
        'Average number of customers in the system': l,
        'Average number of customers in the queue': lq,
        'Average waiting time in the system': w,
        'Average waiting time in the queue': wq
    }
    print(results)
    return lq, wq, l, w, utilization



from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("850x519")
window.configure(bg = "#3A7FF6")

def submit_handler():
    queuing = str(entry_1.get())
    Sigma = float(entry_2.get())
    st2 = int(entry_3.get())
    st1 = int(entry_4.get())
    C = int(entry_5.get())
    L = float(entry_6.get())
    mew = float(entry_7.get())
    #canvas.itemconfig(tagOrId=RHO, text=mew)
    match queuing:
        case "MM":
            arr1, num_of_cust = CP(L)
            arr2 = CPlookUp(L, num_of_cust)
            IA = IAMM(arr1, arr2, num_of_cust)
            arrivals = [0]
            Arrivals(arrivals, IA, num_of_cust)
            IA.insert(0, 0)
            service = ServiceMM(num_of_cust, mew)
            wt, rt, ta = qeueing(num_of_cust, arrivals, service)
            lq, wq, l, w, rho = mmc(L, mew, C)
            canvas.itemconfig(tagOrId=AWT, text=str(wt))
            canvas.itemconfig(tagOrId=ART, text=str(rt))
            canvas.itemconfig(tagOrId=ATA, text=str(ta))
            canvas.itemconfig(tagOrId=LQ, text=str(lq))
            canvas.itemconfig(tagOrId=WQ, text=str(wq))
            canvas.itemconfig(tagOrId=LE, text=str(l))
            canvas.itemconfig(tagOrId=W, text=str(w))
            canvas.itemconfig(tagOrId=RHO, text=str(rho))
            plt.show()

        case "MG":
            arr1, num_of_cust = CP(L)
            arr2 = CPlookUp(L, num_of_cust)
            IA = IAMG(arr1, arr2, num_of_cust, mew)
            arrivals = [0]
            Arrivals(arrivals, IA, num_of_cust)
            IA.insert(0, 0)
            service = ServiceMG(num_of_cust, mew, Sigma)
            wt, rt, ta = qeueing(num_of_cust, arrivals, service)
            lq, wq, l, w, rho = mgc(L, mew, C)
            canvas.itemconfig(tagOrId=AWT, text=str(wt))
            canvas.itemconfig(tagOrId=ART, text=str(rt))
            canvas.itemconfig(tagOrId=ATA, text=str(ta))
            canvas.itemconfig(tagOrId=LQ, text=str(lq))
            canvas.itemconfig(tagOrId=WQ, text=str(wq))
            canvas.itemconfig(tagOrId=LE, text=str(l))
            canvas.itemconfig(tagOrId=W, text=str(w))
            canvas.itemconfig(tagOrId=RHO, text=str(rho))
            plt.show()

        case "GG":
            arr1, num_of_cust = CP(L)
            arr2 = CPlookUp(L, num_of_cust)
            IA = IAGG(arr1, arr2, num_of_cust, mew)
            arrivals = [0]
            Arrivals(arrivals, IA, num_of_cust)
            IA.insert(0, 0)
            service = ServiceGG(num_of_cust, st1, st2)
            wt, rt, ta = qeueing(num_of_cust, arrivals, service)
            lq, wq, l, w, rho = ggc(L, st1, st2, C, mew)
            canvas.itemconfig(tagOrId=AWT, text=str(wt))
            canvas.itemconfig(tagOrId=ART, text=str(rt))
            canvas.itemconfig(tagOrId=ATA, text=str(ta))
            canvas.itemconfig(tagOrId=LQ, text=str(lq))
            canvas.itemconfig(tagOrId=WQ, text=str(wq))
            canvas.itemconfig(tagOrId=LE, text=str(l))
            canvas.itemconfig(tagOrId=W, text=str(w))
            canvas.itemconfig(tagOrId=RHO, text=str(rho))
            plt.show()

canvas = Canvas(
    window,
    bg = "#3A7FF6",
    height = 519,
    width = 850,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    75.0,
    850.0,
    505.0,
    fill="#FCFCFC",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=submit_handler,
    relief="flat"
)
button_1.place(
    x=661.0,
    y=452.0,
    width=170.0,
    height=35.0
)

canvas.create_text(
    16.0,
    21.0,
    anchor="nw",
    text="Simulation and Modelling",
    fill="#FFFFFF",
    font=("Roboto Bold", 30 * -1)
)

canvas.create_text(
    16.0,
    92.0,
    anchor="nw",
    text="Queuing",
    fill="#505485",
    font=("RobotoRoman SemiBold", 16 * -1)
)

canvas.create_rectangle(
    0.0,
    74.0,
    850.0,
    76.0,
    fill="#022569",
    outline="")

canvas.create_rectangle(
    0.0,
    504.0,
    850.0,
    506.0,
    fill="#022569",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    101.0,
    128.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=22.0,
    y=111.0,
    width=158.0,
    height=33.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    101.0,
    256.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=22.0,
    y=239.0,
    width=158.0,
    height=33.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    292.0,
    256.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=213.0,
    y=239.0,
    width=158.0,
    height=33.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    292.0,
    320.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=213.0,
    y=303.0,
    width=158.0,
    height=33.0
)

canvas.create_text(
    207.0,
    92.0,
    anchor="nw",
    text="No. of Servers",
    fill="#505485",
    font=("RobotoRoman SemiBold", 16 * -1)
)

canvas.create_text(
    16.0,
    308.0,
    anchor="nw",
    text="Results:",
    fill="#505485",
    font=("RobotoRoman Medium", 22 * -1)
)

canvas.create_text(
    16.0,
    356.0,
    anchor="nw",
    text="Avg wait time:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    16.0,
    399.0,
    anchor="nw",
    text="Avg response time:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    16.0,
    442.0,
    anchor="nw",
    text="Avg time of arrival:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    425.0,
    92.0,
    anchor="nw",
    text="LQ:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    425.0,
    140.0,
    anchor="nw",
    text="L:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    425.0,
    116.0,
    anchor="nw",
    text="WQ:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    425.0,
    164.0,
    anchor="nw",
    text="W:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

canvas.create_text(
    425.0,
    188.0,
    anchor="nw",
    text="RHO:",
    fill="#505485",
    font=("RobotoRoman Medium", 16 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    292.0,
    128.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=213.0,
    y=111.0,
    width=158.0,
    height=33.0
)

canvas.create_text(
    16.0,
    156.0,
    anchor="nw",
    text="Arrival Rate",
    fill="#505485",
    font=("RobotoRoman SemiBold", 16 * -1)
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    101.0,
    192.5,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=22.0,
    y=175.0,
    width=158.0,
    height=33.0
)

canvas.create_text(
    207.0,
    156.0,
    anchor="nw",
    text="Service Rate",
    fill="#505485",
    font=("RobotoRoman SemiBold", 16 * -1)
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    292.0,
    192.5,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#E8EDF9",
    fg="#000716",
    highlightthickness=0
)
entry_7.place(
    x=213.0,
    y=175.0,
    width=158.0,
    height=33.0
)

canvas.create_text(
    16.0,
    219.0,
    anchor="nw",
    text="Sigma",
    fill="#515486",
    font=("RobotoRoman SemiBold", 16 * -1)
)

AWT = canvas.create_text(
    168.0,
    356.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

ART = canvas.create_text(
    168.0,
    399.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

ATA = canvas.create_text(
    168.0,
    442.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

WQ = canvas.create_text(
    504.0,
    116.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

LE = canvas.create_text(
    504.0,
    140.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

W = canvas.create_text(
    504.0,
    165.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

RHO = canvas.create_text(
    504.0,
    188.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

LQ = canvas.create_text(
    504.0,
    92.0,
    anchor="nw",
    text="0",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)

canvas.create_text(
    210.0,
    216.0,
    anchor="nw",
    text="Upper bound",
    fill="#515486",
    font=("RobotoRoman SemiBold", 16 * -1)
)

canvas.create_text(
    211.0,
    283.0,
    anchor="nw",
    text="Lower bound",
    fill="#515486",
    font=("RobotoRoman SemiBold", 16 * -1)
)

canvas.create_text(
    653.0,
    334.0,
    anchor="nw",
    text="Syed Shaheer Ali Zaidi\nIlhaam Ismail Soomro\nMohammad Tahir\nSaad Shariq\nMohammad Noor Sheikh\nRabi Ahmed",
    fill="#000000",
    font=("RobotoRoman SemiBold", 16 * -1)
)
window.resizable(False, False)
window.mainloop()
