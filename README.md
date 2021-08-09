# RWKV-LM

We propose the RWKV language model, with alternating time-mix and channel-mix layers:

<img src=
"https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cbegin%7Balign%2A%7D%0A%5Ctext%7BTime-mix+%3A%7D+%26%26+%5Ctext%7BTM%7D_%7Bt%2Cc%7D+%26%26%3D%26%26%5Ctext%7Bsigmoid%7D%28%5Ctext%7BR%7D_%7Bt%2Cc%7D%29+%26%26%5Ccdot%26%26+%26%26%5Ctextstyle%5Csum_%7Bu%7D+%26%26%5Ctextbf%7BW%7D_%7Bt%2Cu%2Cc%7D+%26%26%5Ccdot%26%26+%5Ctext%7Bsoftmax%7D_t%28%5Ctext%7BK%7D_%7Bu%2Cc%7D%29+%26%26%5Ccdot%26%26+%5Ctext%7BV%7D_%7Bu%2Cc%7D%5C%5C%0A%5Ctext%7BChannel-mix+%3A%7D+%26%26+%5Ctext%7BCM%7D_%7Bt%2Cc%7D+%26%26%3D%26%26%5Ctext%7Bsigmoid%7D%28%5Ctext%7BR%7D_%7Bt%2Cc%7D%29+%26%26%5Ccdot%26%26+%26%26%5Ctextstyle%5Csum_d+%26%26%5Ctextbf%7BW%7D_%7Bc%2Cd%7D+%26%26%5Ccdot%26%26+%5Ctext%7Bgelu%7D%28%5Ctext%7BK%7D_%7Bt%2Cd%7D%29+%26%26%5Ccdot%26%26+%5Ctext%7BV%7D_%7Bt%2Cd%7D%0A%5Cend%7Balign%2A%7D%0A" 
alt="\begin{align*}
\text{Time-mix :} && \text{TM}_{t,c} &&=&&\text{sigmoid}(\text{R}_{t,c}) &&\cdot&& &&\textstyle\sum_{u} &&\textbf{W}_{t,u,c} &&\cdot&& \text{softmax}_t(\text{K}_{u,c}) &&\cdot&& \text{V}_{u,c}\\
\text{Channel-mix :} && \text{CM}_{t,c} &&=&&\text{sigmoid}(\text{R}_{t,c}) &&\cdot&& &&\textstyle\sum_d &&\textbf{W}_{c,d} &&\cdot&& \text{gelu}(\text{K}_{t,d}) &&\cdot&& \text{V}_{t,d}
\end{align*}
">

* Here R, K, V are generated by linear transforms of input, and W is parameter. Basically RWKV decomposes attention into R(target) * W(src, target) * K(src). So we can call R "receptance", and sigmoid means it's in 0~1 range.

* The Time-mix is similar to AFT (https://arxiv.org/abs/2105.14103). There are two differences.

(1) We changed the normalization (denominator). For masked language models, we define:

<img src=
"https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctext%7Bsoftmax%7D_t%28%5Ctext%7BK%7D_%7Bu%2Cc%7D%29+%3D+%5Cfrac%7B%5Cexp%28%5Ctext%7BK%7D_%7Bu%2Cc%7D%29%7D%7B%5Csum_%7Bv+%5Cleq+t%7D%5Cexp%28%5Ctext%7BK%7D_%7Bv%2Cc%7D%29%7D" 
alt="\text{softmax}_t(\text{K}_{u,c}) = \frac{\exp(\text{K}_{u,c})}{\sum_{v \leq t}\exp(\text{K}_{v,c})}">  
 
(2) We decompose W_{t,u,c} and introduce multi-head W (here h is the corresponding head of c):

<img src=
"https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+W_%7Bt%2Cu%2Cc%7D%3Df_h%28t-u%29%5Ccdot+%5Calpha_h%28u%29+%5Ccdot+%5Cbeta_h%28t%29" 
alt="W_{t,u,c}=f_h(t-u)\cdot \alpha_h(u) \cdot \beta_h(t)">

Moreover we multiply the final output of Time-mix layer by γ(t). The reason for the α β γ factors, is because the context size is smaller when t is small, and this can be compensated using the α β γ factors.

* The Channel-mix is similar to GeGLU (https://arxiv.org/abs/2002.05202) with an extra R factor.

* Finally, we add extra time-mixing as in (https://github.com/BlinkDL/minGPT-tuned). You can try reducing the amt of time-mixing in upper layers of deep models.

***

We also propose a new sampling method (as in src/utils.py):

(1) Find the max probability p_max after softmax.

(2) Remove all entries whose probability is lower than 0.02 * pow(p_max, 2)

(3) Feel free to tune the 0.02 and 2 factor.

***

Training loss, RWKV vs MHA+Rotary+GeGLU:

![RWKV-vs-MHA](RWKV-vs-MHA.png)

(this is character-level loss with simplebooks-92 dataset https://dldata-public.s3.us-east-2.amazonaws.com/simplebooks.zip)
