# Community Helm Charts

This repository hosts a collection of community-maintained Helm charts.

## 🚀 Usage

### Add Helm Repository

To start using the charts, add the repository to your Helm client:

```bash
helm repo add mondu-ai https://mondu-ai.github.io/helm-charts-community
helm repo update
```

Replace `mondu-ai` with a name you want to use for this repository locally, and `mondu-ai` with your actual GitHub username.

### Install a Chart

Once the repository is added, you can install any chart from this collection. For example, to install the `example-chart`:

```bash
helm install my-release mondu-ai/example-chart
```

Replace `my-release` with a name for your release and `example-chart` with the name of the chart you want to install. You can find the list of available charts in the `charts/` directory or by searching the repository.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
