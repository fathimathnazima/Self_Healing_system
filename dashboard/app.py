import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json, os
import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Self-Healing Cloud Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=5000,key="refresh")


# -----------------------------------
# CUSTOM STYLING
# -----------------------------------

st.markdown("""
<style>
.main{
background:#0f172a;
color:white;
}

.block-container{
padding-top:1rem;
max-width:1450px;
}

div[data-testid="metric-container"]{
background:#111827;
padding:18px;
border-radius:18px;
border:1px solid #334155;
box-shadow:0 4px 14px rgba(0,0,0,.25);
}

h1,h2,h3{
color:#f8fafc;
}

.alert-box{
padding:16px;
border-radius:16px;
background:linear-gradient(90deg,#0ea5e9,#2563eb);
color:white;
font-weight:600;
}

.good{
padding:15px;
border-radius:14px;
background:#052e16;
border:1px solid #16a34a;
}

.bad{
padding:15px;
border-radius:14px;
background:#450a0a;
border:1px solid #ef4444;
}
</style>
""",unsafe_allow_html=True)


# -----------------------------------
# PATHS
# -----------------------------------

BASE_DIR=os.path.dirname(
os.path.dirname(
os.path.abspath(__file__)
))

STATS_FILE=os.path.join(
BASE_DIR,
"stats.json"
)

LOG_FILE=os.path.join(
BASE_DIR,
"logs",
"system.log"
)


# -----------------------------------
# LOAD DATA
# -----------------------------------

if os.path.exists(STATS_FILE):
    with open(STATS_FILE) as f:
        stats=json.load(f)
else:
    stats={}


# -----------------------------------
# HERO HEADER
# -----------------------------------

st.markdown("""
<div class='alert-box'>
🛡 AI-Driven Self-Healing Cloud Monitoring Platform  
Real-Time Monitoring • Automated Recovery • Risk Analytics
</div>
""",unsafe_allow_html=True)

st.write("")


# -----------------------------------
# KPIs
# -----------------------------------

total_services=len(stats)

total_failures=sum(
stats[s].get("failures",0)
for s in stats
)

unstable=sum(
1 for s in stats
if stats[s].get("failures",0)>=3
)

healthy=total_services-unstable


if total_failures==0:
    health_score=100
else:
    health_score=max(
    100-total_failures*2,
    50
    )


# -----------------------------------
# STATUS BANNER
# -----------------------------------

if unstable>0:
    st.markdown("""
<div class='bad'>
🔴 SYSTEM DEGRADED — Critical services require attention
</div>
""",unsafe_allow_html=True)

else:
    st.markdown("""
<div class='good'>
🟢 SYSTEM OPERATIONAL — All monitored services healthy
</div>
""",unsafe_allow_html=True)


st.write("")


# -----------------------------------
# KPI CARDS
# -----------------------------------

c1,c2,c3,c4,c5=st.columns(5)

c1.metric(
"Services",
total_services
)

c2.metric(
"Failures",
total_failures
)

c3.metric(
"Unstable",
unstable
)

c4.metric(
"Healthy",
healthy
)

c5.metric(
"Health Score",
f"{health_score}%"
)


st.divider()


# -----------------------------------
# BUILD DATAFRAME
# -----------------------------------

rows=[]

for service,data in stats.items():

    failures=data.get("failures",0)

    if failures<=2:
        risk="LOW"
        status="🟢 Healthy"

    elif failures<=5:
        risk="MEDIUM"
        status="🟡 Warning"

    else:
        risk="HIGH"
        status="🔴 Critical"


    rows.append({
        "Service":service,
        "Failures":failures,
        "Risk":risk,
        "Status":status,
        "Last Restart":
            data.get(
            "last_restart",
            "-"
            ),
        "Last Seen":
            data.get(
            "last_seen",
            "-"
            )
    })


df=pd.DataFrame(rows)



# -----------------------------------
# EXECUTIVE SUMMARY
# -----------------------------------

left,right=st.columns([2,1])

with left:

    st.subheader(
    "🖥 Service Health Matrix"
    )

    if not df.empty:
        st.dataframe(
        df,
        width="stretch"
        )

with right:

    st.subheader(
    "⚙ Stability Gauge"
    )

    st.progress(
    health_score/100
    )

    st.write(
    f"Estimated Stability: {health_score}%"
    )


st.divider()



# -----------------------------------
# ANALYTICS
# -----------------------------------

a1,a2=st.columns(2)

with a1:
    st.subheader(
    "📈 Failure Analytics"
    )

    if not df.empty:
        st.bar_chart(
        df.set_index(
        "Service"
        )["Failures"]
        )


with a2:
    st.subheader(
    "🚨 Risk Distribution"
    )

    if not df.empty:
        st.bar_chart(
        df["Risk"].value_counts()
        )


st.divider()


# -----------------------------------
# INCIDENT FEED
# -----------------------------------

st.subheader(
"🚨 Incident Feed"
)

if not df.empty:

    critical=df[
    df["Risk"]=="HIGH"
    ]

    if not critical.empty:

        for s in critical["Service"]:
            st.error(
            f"{s} flagged as critical"
            )

    else:
        st.success(
        "No active critical incidents."
        )


st.divider()


# -----------------------------------
# LIVE LOGS
# -----------------------------------

st.subheader(
"📄 Live System Logs"
)

if os.path.exists(
LOG_FILE
):
    with open(
    LOG_FILE
    ) as f:
        logs=f.read()

    st.text_area(
    "",
    logs[-5000:],
    height=350
    )


st.divider()


# -----------------------------------
# FOOTER
# -----------------------------------

st.caption("""
Prototype AI-Driven Self-Healing Cloud Monitoring Platform  
Built with Python • Streamlit • Automated Recovery Analytics
""")