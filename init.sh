#!/bin/bash



## --------------------------------------------------------------------------
## 定数定義
## --------------------------------------------------------------------------

PRJ_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd);

PYTHON_EXEC_IMAGE='3.11.1-alpine3.17';
PRE_EXEC_SCRIPT_AARCH64="\
	apk add \
	  --no-cache \
	  --update-cache \
	  --virtual .exec_pip_dependencies \
	    alpine-sdk \
	    musl-dev \
	    libffi-dev \
	 && \
	apk add \
	  --no-cache \
	  --update-cache \
	  --virtual .install_pip_requirements_dependencies \
	    alpine-sdk";
PRE_EXEC_SCRIPT="\
	pip install --upgrade pip \
	 && \
	pip install -r requirements.txt";
POST_EXEC_SCRIPT_AARCH64="\
	apk del --purge .install_pip_requirements_dependencies";
[ "$(arch)" = 'aarch64' ] && PRE_EXEC_SCRIPT="\
	${PRE_EXEC_SCRIPT_AARCH64} \
	 && \
	${PRE_EXEC_SCRIPT} \
	 && \
	${POST_EXEC_SCRIPT_AARCH64}";
EXEC_SCRIPT_APP="${PRE_EXEC_SCRIPT} && python app.py";
EXEC_SCRIPT_SH="${PRE_EXEC_SCRIPT} && sh";
EXEC_SCRIPT_DB_UPGRADE="${PRE_EXEC_SCRIPT} && flask db upgrade";



## --------------------------------------------------------------------------
## 開発に使用するコマンドの定義
## --------------------------------------------------------------------------

## Docker 起動のための共通処理
_exec() {
	docker run --rm \
		-p '8080:8080' \
		-e "FLASK_APP=app.py" \
		-v "${PRJ_DIR}:/geolocation_test" \
		--workdir "/geolocation_test" \
		-it python:${PYTHON_EXEC_IMAGE} \
			sh "${@}";
}

## Docker で flask db upgrade を実行
exec_db_upgrade() { _exec -c "${EXEC_SCRIPT_DB_UPGRADE}"; }

## Docker で app.py を起動
exec_app() { _exec -c "${EXEC_SCRIPT_APP}"; }

## Docker で開発環境のシェルを起動
exec_sh() { _exec -c "${EXEC_SCRIPT_SH}"; }

download_statics() {
	declare -A ESM_JS_LIST=(
		['socket.io.esm.min.js']='https://cdn.socket.io/4.3.2/socket.io.esm.min.js'
		['vue.esm-browser.js']='https://unpkg.com/vue@3.2.47/dist/vue.esm-browser.js'
	);

	for ESM_JS in ${!ESM_JS_LIST[@]};
	do
		curl --output "${PRJ_DIR}/static/${ESM_JS}" ${ESM_JS_LIST[${ESM_JS}]}
	done
}