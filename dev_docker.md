# docker 统一开发环境

## 一键安装docker

```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

## 下载镜像
```bash
###登录阿里云镜像服务器
docker login registry.cn-hangzhou.aliyuncs.com
```


账号密码
```
username:guest_01@1725738280819274
password:uni123456
```

拉取latest镜像
```bash
docker pull registry.cn-hangzhou.aliyuncs.com/uni_smart_drive/dev:latest
```


## 安装nvidia docker plugin（可选，需要使用GPU运行感知模块）
```bash
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   
 sudo apt-get update && apt-get install -y nvidia-docker2

 sudo systemctl restart docker
```

验证安装，是否能输出gpu信息
```bash
sudo docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```
看是否能输出gpu信息，能输出则安装成功



## 启动容器
```bash
# --gpus all 需要安装上述nvidia docker plugin，非必须
docker run -it \
 --gpus all \
 --network host \
 --volume="/home/$USER:/home/$USER" \
 --name=dev \
 --privileged=true \
 registry.cn-hangzhou.aliyuncs.com/uni_smart_drive/dev:latest\
 bash 
```

#再次进入容器
```bash
docker exec -it dev bash 
```

#退出容器
```bash
exit
```

## 运⾏功能模块
1. 在容器外部运⾏roscore
2. 在容器内部运⾏各种模块, 例如:
```bash
run_perception
```


可视化调试：在容器外部运⾏rviz

ps. 宿主机的ros需要先安装ros-noetic-jsk-recognition-msgs 和 ros-melodic-jsk-rviz-plugins
来可视化感知结果
```bash
sudo apt-get install ros-noetic-jsk-recognition-msgs ros-melodic-jsk-rviz-plugins
```

```bash
roslaunch rviz rviz.launch
```
